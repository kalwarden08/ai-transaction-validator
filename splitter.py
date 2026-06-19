"""
CSV splitting utility for large validated datasets.
"""
import os
import pandas as pd
from typing import List


class CSVSplitter:
    """Splits CSV files into chunks based on row count."""

    @staticmethod
    def split_csv(df: pd.DataFrame, output_dir: str, chunk_size: int = 1000, prefix: str = "chunk") -> List[str]:
        """
        Split DataFrame into multiple CSV files.
        
        Args:
            df: DataFrame to split
            output_dir: Directory to save chunk files
            chunk_size: Number of rows per chunk
            prefix: Prefix for chunk filenames
            
        Returns:
            List of created filenames
        """
        if df.empty:
            return []

        os.makedirs(output_dir, exist_ok=True)
        filenames = []

        # Calculate number of chunks needed
        total_rows = len(df)
        num_chunks = (total_rows + chunk_size - 1) // chunk_size

        # Split and save chunks
        for i in range(num_chunks):
            start_idx = i * chunk_size
            end_idx = min((i + 1) * chunk_size, total_rows)
            
            chunk_df = df.iloc[start_idx:end_idx]
            chunk_filename = f"{prefix}_{i + 1}.csv"
            chunk_path = os.path.join(output_dir, chunk_filename)
            
            chunk_df.to_csv(chunk_path, index=False)
            filenames.append(chunk_filename)

        return filenames

    @staticmethod
    def get_split_info(df: pd.DataFrame, chunk_size: int = 1000) -> dict:
        """
        Get information about how many chunks would be created.
        
        Args:
            df: DataFrame to analyze
            chunk_size: Number of rows per chunk
            
        Returns:
            Dictionary with split information
        """
        total_rows = len(df)
        num_chunks = (total_rows + chunk_size - 1) // chunk_size if total_rows > 0 else 0

        return {
            'total_rows': total_rows,
            'chunk_size': chunk_size,
            'num_chunks': num_chunks,
            'will_split': num_chunks > 1
        }
