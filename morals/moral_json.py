#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from pathlib import Path
from typing import Dict, Any
from .moral_context import MoralContext, JSONEncoder

class MoralContextManager:
	"""Manages saving and loading MoralContext instances to/from JSON files"""
	
	def __init__(self, data_dir: str = "moral_data"):
		self.data_dir = Path(data_dir)
		self.data_dir.mkdir(exist_ok=True)
	
	def save_context(self, context: MoralContext, name: str) -> str:
		"""Save a MoralContext to JSON file"""
		filename = f"{name}.json"
		filepath = self.data_dir / filename
		context.to_json(str(filepath))
		return str(filepath)
	
	def load_context(self, name: str) -> MoralContext:
		"""Load a MoralContext from JSON file"""
		filename = f"{name}.json"
		filepath = self.data_dir / filename
		return MoralContext.from_json(str(filepath))
	
	def list_contexts(self) -> list[str]:
		"""List all available MoralContext files"""
		return [f.stem for f in self.data_dir.glob("*.json")]
	
	def context_exists(self, name: str) -> bool:
		"""Check if a MoralContext file exists"""
		return (self.data_dir / f"{name}.json").exists()
