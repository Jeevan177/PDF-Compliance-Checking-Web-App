from langchain_community.document_loaders import PDFPlumberLoader
from langchain.chains.question_answering import load_qa_chain
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import CharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
import os
import tempfile
import aiofiles
from typing import Dict, Any
from fastapi import UploadFile
import logging
import re

logger = logging.getLogger(__name__)

class ComplianceService:
    def __init__(self):
        self.groq_api_key = os.environ.get("GROQ_API_KEY")
        if not self.groq_api_key:
            raise EnvironmentError("GROQ_API_KEY environment variable is not set.")
        
        # Initialize embeddings (can be cached)
        self.embeddings = HuggingFaceEmbeddings(
            model_name="all-MiniLM-L6-v2", 
            model_kwargs={"device": "cpu"}
        )
    
    async def load_documents(self, file_obj: UploadFile):
        """Load PDF documents using temporary file"""
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            content = await file_obj.read()
            temp_file.write(content)
            temp_path = temp_file.name
        
        try:
            loader = PDFPlumberLoader(temp_path)
            docs = loader.load()
            return docs
        finally:
            # Clean up temp file
            if os.path.exists(temp_path):
                os.unlink(temp_path)
    
    def get_vectorstore(self, docs):
        """Create vector store from documents"""
        splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        chunks = splitter.split_documents(docs)
        return FAISS.from_documents(chunks, self.embeddings)
    
    def create_qa_chain(self):
        """Create QA chain with Groq LLM"""
        llm = ChatGroq(
            groq_api_key=self.groq_api_key, 
            model="deepseek-r1-distill-llama-70b"
        )
        return load_qa_chain(llm=llm, chain_type="stuff")
    
    def clean_and_format_response(self, response: str) -> str:
        """Clean response by removing <think> tags and formatting as points"""
        # Remove <think> and </think> tags and their content
        cleaned_response = re.sub(r'<think>.*?</think>', '', response, flags=re.DOTALL | re.IGNORECASE)
        
        # Remove any remaining think tags variations
        cleaned_response = re.sub(r'</?think[^>]*>', '', cleaned_response, flags=re.IGNORECASE)
        
        # Clean up extra whitespace
        cleaned_response = re.sub(r'\s+', ' ', cleaned_response).strip()
        
        # If response is empty after cleaning, return a default message
        if not cleaned_response:
            return "• No clear assessment could be provided for this rule."
        
        # Format as bullet points if not already formatted
        if not self.is_already_formatted(cleaned_response):
            return self.format_as_points(cleaned_response)
        
        return cleaned_response
    
    def is_already_formatted(self, text: str) -> bool:
        """Check if text is already formatted with bullet points or numbers"""
        # Check for various bullet point formats
        bullet_patterns = [
            r'^\s*[•·▪▫‣⁃]\s',  # Unicode bullets
            r'^\s*[-*]\s',       # Dash or asterisk bullets
            r'^\s*\d+\.\s',      # Numbered points
            r'^\s*[a-zA-Z]\.\s', # Lettered points
        ]
        
        lines = text.split('\n')
        formatted_lines = 0
        
        for line in lines:
            line = line.strip()
            if line:  # Only check non-empty lines
                for pattern in bullet_patterns:
                    if re.match(pattern, line):
                        formatted_lines += 1
                        break
        
        # If more than 30% of non-empty lines are formatted, consider it already formatted
        non_empty_lines = len([line for line in lines if line.strip()])
        return non_empty_lines > 0 and (formatted_lines / non_empty_lines) > 0.3
    
    def format_as_points(self, text: str) -> str:
        """Format text as bullet points"""
        # Split text into sentences or logical chunks
        sentences = self.split_into_logical_points(text)
        
        if len(sentences) <= 1:
            # If only one sentence, just add a bullet point
            return f"• {text}"
        
        # Format each point with bullet
        formatted_points = []
        for sentence in sentences:
            sentence = sentence.strip()
            if sentence:
                # Remove any existing bullet points
                sentence = re.sub(r'^\s*[•·▪▫‣⁃\-*]\s*', '', sentence)
                formatted_points.append(f"• {sentence}")
        
        return '\n'.join(formatted_points)
    
    def split_into_logical_points(self, text: str) -> list:
        """Split text into logical points for bullet formatting"""
        # First, try to split by common separators
        separators = ['. ', '; ', ', and ', ', or ', ' Also, ', ' Additionally, ', ' Furthermore, ', ' Moreover, ']
        
        points = [text]
        
        for separator in separators:
            new_points = []
            for point in points:
                if separator in point:
                    split_points = point.split(separator)
                    for i, split_point in enumerate(split_points):
                        split_point = split_point.strip()
                        if split_point:
                            # Add period back if it was removed by splitting on '. '
                            if separator == '. ' and i < len(split_points) - 1 and not split_point.endswith('.'):
                                split_point += '.'
                            new_points.append(split_point)
                else:
                    new_points.append(point)
            points = new_points
        
        # Filter out very short points (likely incomplete)
        points = [point.strip() for point in points if len(point.strip()) > 10]
        
        # If we ended up with too many small points, recombine
        if len(points) > 5:
            return [text]  # Return original text as single point
        
        return points if points else [text]
    
    async def run_compliance_check(self, pdf_file_obj: UploadFile, rules_file_obj: UploadFile) -> Dict[str, Any]:
        """Run compliance check against rules"""
        try:
            logger.info("Loading PDF documents...")
            docs = await self.load_documents(pdf_file_obj)
            
            logger.info("Creating vector store...")
            vectorstore = self.get_vectorstore(docs)
            
            logger.info("Creating QA chain...")
            chain = self.create_qa_chain()
            
            logger.info("Reading rules file...")
            rules_content = await rules_file_obj.read()
            rules_text = rules_content.decode('utf-8')
            rules = [line.strip() for line in rules_text.splitlines() if line.strip()]
            
            logger.info(f"Processing {len(rules)} rules...")
            results = {}
            
            for i, rule in enumerate(rules, 1):
                logger.info(f"Processing rule {i}/{len(rules)}: {rule[:50]}...")
                try:
                    # Create a more specific prompt for better responses
                    enhanced_question = f"""
                    Based on the document content, please analyze the following compliance rule and provide a clear assessment:
                    
                    Rule: {rule}
                    
                    Please provide your response in a structured format focusing on:
                    1. Whether the rule is met or not
                    2. Specific evidence from the document
                    3. Any relevant details or exceptions
                    
                    Keep your response concise and factual.
                    """
                    
                    answer = chain.run(input_documents=docs, question=enhanced_question)
                    
                    # Clean and format the response
                    formatted_answer = self.clean_and_format_response(answer)
                    results[rule] = formatted_answer
                    
                except Exception as e:
                    logger.error(f"Error processing rule '{rule}': {str(e)}")
                    results[rule] = f"• Error processing rule: {str(e)}"
            
            return results
            
        except Exception as e:
            logger.error(f"Error in compliance check: {str(e)}")
            raise
    
    # async def run_compliance_check(self, pdf_file_obj: UploadFile, rules_file_obj: UploadFile) -> Dict[str, Any]:
    #     """Run compliance check against rules"""
    #     try:
    #         logger.info("Loading PDF documents...")
    #         docs = await self.load_documents(pdf_file_obj)
            
    #         logger.info("Creating vector store...")
    #         vectorstore = self.get_vectorstore(docs)
            
    #         logger.info("Creating QA chain...")
    #         chain = self.create_qa_chain()
            
    #         logger.info("Reading rules file...")
    #         rules_content = await rules_file_obj.read()
    #         rules_text = rules_content.decode('utf-8')
    #         rules = [line.strip() for line in rules_text.splitlines() if line.strip()]
            
    #         logger.info(f"Processing {len(rules)} rules...")
    #         results = {}
            
    #         for i, rule in enumerate(rules, 1):
    #             logger.info(f"Processing rule {i}/{len(rules)}: {rule[:50]}...")
    #             try:
    #                 answer = chain.run(input_documents=docs, question=rule)

    #                 results[rule] = answer
    #             except Exception as e:
    #                 logger.error(f"Error processing rule '{rule}': {str(e)}")
    #                 results[rule] = f"Error processing rule: {str(e)}"
            
    #         return results
            
    #     except Exception as e:
    #         logger.error(f"Error in compliance check: {str(e)}")
    #         raise