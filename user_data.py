import json
import os
from datetime import datetime, timedelta
from collections import defaultdict

class UserHistory:
    def __init__(self):
        self.history_file = "user_history.json"
        self.stats_file = "usage_stats.json"
        self._ensure_data_directory()
        self.load_history()
        self.load_stats()

    def _ensure_data_directory(self):
        """Ensure the data directory exists"""
        data_dir = "data"
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
        self.history_file = os.path.join(data_dir, self.history_file)
        self.stats_file = os.path.join(data_dir, self.stats_file)

    def load_history(self):
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    self.history = json.load(f)
            except Exception as e:
                print(f"Error loading history: {e}")
                self.history = []
        else:
            self.history = []

    def load_stats(self):
        if os.path.exists(self.stats_file):
            try:
                with open(self.stats_file, 'r', encoding='utf-8') as f:
                    self.stats = json.load(f)
            except Exception as e:
                print(f"Error loading stats: {e}")
                self.stats = self._initialize_stats()
        else:
            self.stats = self._initialize_stats()

    def _initialize_stats(self):
        return {
            "total_rewrites": 0,
            "daily_usage": {},
            "avg_text_length": 0,
            "total_characters": 0,
            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

    def save_history(self):
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(self.history, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error saving history: {e}")

    def save_stats(self):
        try:
            self.stats["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open(self.stats_file, 'w', encoding='utf-8') as f:
                json.dump(self.stats, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error saving stats: {e}")

    def add_entry(self, original_text, rewritten_text):
        try:
            # Add to history
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            date = timestamp.split()[0]
            
            entry = {
                'timestamp': timestamp,
                'original': original_text,
                'rewritten': rewritten_text,
                'char_count': len(original_text)
            }
            self.history.append(entry)
            
            # Update stats
            self.stats["total_rewrites"] += 1
            self.stats["daily_usage"][date] = self.stats["daily_usage"].get(date, 0) + 1
            self.stats["total_characters"] += len(original_text)
            self.stats["avg_text_length"] = self.stats["total_characters"] / self.stats["total_rewrites"]
            
            # Save both history and stats
            self.save_history()
            self.save_stats()
            
            return True
        except Exception as e:
            print(f"Error adding entry: {e}")
            return False

    def get_usage_stats(self):
        return self.stats

    def get_daily_usage(self, days=7):
        daily_usage = defaultdict(int)
        end_date = datetime.now()
        
        # Ensure we have entries for all days
        for i in range(days):
            date = (end_date - timedelta(days=i)).strftime("%Y-%m-%d")
            daily_usage[date] = self.stats["daily_usage"].get(date, 0)
        
        # Sort by date
        return dict(sorted(daily_usage.items()))

    def clear_history(self):
        try:
            self.history = []
            self.stats = self._initialize_stats()
            self.save_history()
            self.save_stats()
            return True
        except Exception as e:
            print(f"Error clearing history: {e}")
            return False

    def get_history(self):
        return self.history

    def get_stats_summary(self):
        """Get a summary of usage statistics"""
        return {
            "total_rewrites": self.stats["total_rewrites"],
            "total_characters": self.stats["total_characters"],
            "avg_text_length": round(self.stats["avg_text_length"], 2),
            "last_updated": self.stats.get("last_updated", "Never")
        } 