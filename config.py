# config.py
import os
from dotenv import load_dotenv
import logging
from typing import Optional

# Load environment variables
load_dotenv()

class BankingConfig:
    """Centralized configuration for the banking agent system"""
    
    def __init__(self):
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")
        if not self.gemini_api_key:
            raise ValueError("GEMINI_API_KEY environment variable is required")
            
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/openai/"
        self.model_name = "gemini-2.0-flash"
        self.bank_name = "SecureBank International"
        self.bank_code = "SBI"
        
        # Setup logging
        self.setup_logging()
        
        # Initialize provider and model - these will be created when needed
        self._provider = None
        self._model = None
        self._run_config = None
    
    @property
    def provider(self):
        """Lazy loading of provider"""
        if self._provider is None:
            try:
                from agents import AsyncOpenAI
                self._provider = AsyncOpenAI(
                    api_key=self.gemini_api_key,
                    base_url=self.base_url,
                )
            except ImportError as e:
                self.logger.error(f"Failed to import AsyncOpenAI: {e}")
                raise
        return self._provider
    
    @property
    def model(self):
        """Lazy loading of model"""
        if self._model is None:
            try:
                from agents import OpenAIChatCompletionsModel
                self._model = OpenAIChatCompletionsModel(
                    model=self.model_name,
                    openai_client=self.provider
                )
            except ImportError as e:
                self.logger.error(f"Failed to import OpenAIChatCompletionsModel: {e}")
                raise
        return self._model
    
    @property
    def run_config(self):
        """Lazy loading of run config"""
        if self._run_config is None:
            try:
                from agents import RunConfig
                self._run_config = RunConfig(
                    model=self.model,
                    model_provider=self.provider,
                    tracing_disabled=True
                )
            except ImportError as e:
                self.logger.error(f"Failed to import RunConfig: {e}")
                raise
        return self._run_config
    
    def setup_logging(self):
        """Setup professional logging configuration"""
        try:
            logging.basicConfig(
                level=logging.INFO,
                format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                handlers=[
                    logging.FileHandler('banking_agent.log'),
                    logging.StreamHandler()
                ]
            )
            self.logger = logging.getLogger(__name__)
        except Exception as e:
            print(f"Warning: Could not setup file logging: {e}")
            # Fallback to console logging only
            logging.basicConfig(level=logging.INFO)
            self.logger = logging.getLogger(__name__)