import os
from dataclasses import dataclass


@dataclass
class Config:
    timeout: int = 30
    retry: int = 3
    max_workers: int = 5
    user_agent: str = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    output_dir: str = './output'
    image_dir: str = 'images'
    image_width: int = 800


config = Config()
