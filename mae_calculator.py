"""
MAE Calculator for Super Analyst QA System
Calculates Mean Absolute Error between AI and Human analyst scores
"""

from typing import Dict, List, Tuple
from dataclasses import dataclass


@dataclass
class MAEResult:
    """Results from MAE calculation"""
    mae: float
    total_difference: float
    num_kpis: int
    kpi_differences: Dict[str, float]
    interpretation: str
    

def calculate_mae(ai_scores: Dict[str, int], human_scores: Dict[str, int]) -> MAEResult:
    """
    Calculate MAE between AI and human scores for a single chat.
    
    Args:
        ai_scores: Dictionary of KPI names to AI scores (e.g., {"IssueIdentification": 4})
        human_scores: Dictionary of KPI names to human scores
        
    Returns:
        MAEResult object with calculation details
        
    Example:
        >>> ai = {"IssueIdentification": 4, "Clarity": 2, "Sentiment": 3}
        >>> human = {"IssueIdentification": 4, "Clarity": 2, "Sentiment": 4}
        >>> result = calculate_mae(ai, human)
        >>> print(f"MAE: {result.mae:.2f}")
    """
    if set(ai_scores.keys()) != set(human_scores.keys()):
        raise ValueError("AI and human scores must have the same KPIs")
    
    kpi_differences = {}
    total_difference = 0.0
    
    for kpi in ai_scores.keys():
        diff = abs(ai_scores[kpi] - human_scores[kpi])
        kpi_differences[kpi] = diff
        total_difference += diff
    
    num_kpis = len(ai_scores)
    mae = total_difference / num_kpis if num_kpis > 0 else 0.0
    interpretation = interpret_mae(mae)
    
    return MAEResult(
        mae=mae,
        total_difference=total_difference,
        num_kpis=num_kpis,
        kpi_differences=kpi_differences,
        interpretation=interpretation
    )


def interpret_mae(mae: float) -> str:
    """
    Interpret MAE value according to system standards.
    
    Args:
        mae: Mean Absolute Error value
        
    Returns:
        String interpretation of the MAE
    """
    if mae < 0.50:
        return "Excellent (matches human analyst very closely)"
    elif mae < 0.75:
        return "Good (production-ready)"
    elif mae < 1.00:
        return "Acceptable (needs minor calibration)"
    else:
        return "Poor (needs major fixes)"


def calculate_batch_mae(chats: List[Dict]) -> Tuple[float, List[MAEResult]]:
    """
    Calculate MAE across multiple chats.
    
    Args:
        chats: List of dictionaries, each containing:
               - 'chat_id': identifier
               - 'ai_scores': dict of KPI scores
               - 'human_scores': dict of KPI scores
               
    Returns:
        Tuple of (average_mae, list of individual MAEResults)
        
    Example:
        >>> chats = [
        ...     {
        ...         'chat_id': '27811316',
        ...         'ai_scores': {'IssueIdentification': 4, 'Clarity': 2},
        ...         'human_scores': {'IssueIdentification': 4, 'Clarity': 2}
        ...     }
        ... ]
        >>> avg_mae, results = calculate_batch_mae(chats)
    """
    results = []
    
    for chat in chats:
        result = calculate_mae(chat['ai_scores'], chat['human_scores'])
        results.append(result)
    
    avg_mae = sum(r.mae for r in results) / len(results) if results else 0.0
    
    return avg_mae, results


def print_mae_report(chat_id: str, result: MAEResult, ai_scores: Dict[str, int], 
                     human_scores: Dict[str, int]) -> None:
    """
    Print a formatted MAE report for a single chat.
    
    Args:
        chat_id: Chat identifier
        result: MAEResult object
        ai_scores: AI scores dictionary
        human_scores: Human scores dictionary
    """
    print(f"\n{'='*70}")
    print(f"MAE REPORT - ChatID: {chat_id}")
    print(f"{'='*70}")
    print(f"\n{'KPI':<25} {'AI':>5} {'Human':>7} {'|Diff|':>8}")
    print(f"{'-'*70}")
    
    for kpi in ai_scores.keys():
        ai = ai_scores[kpi]
        human = human_scores[kpi]
        diff = result.kpi_differences[kpi]
        print(f"{kpi:<25} {ai:>5} {human:>7} {diff:>8.0f}")
    
    print(f"{'-'*70}")
    print(f"{'Sum of differences:':<25} {result.total_difference:>21.0f}")
    print(f"{'Number of KPIs:':<25} {result.num_kpis:>21}")
    print(f"\n{'MAE:':<25} {result.mae:>21.2f}")
    print(f"{'Interpretation:':<25} {result.interpretation}")
    print(f"{'='*70}\n")


def print_batch_report(avg_mae: float, chat_results: List[Tuple[str, MAEResult]]) -> None:
    """
    Print a summary report for batch MAE calculation.
    
    Args:
        avg_mae: Average MAE across all chats
        chat_results: List of tuples (chat_id, MAEResult)
    """
    print(f"\n{'='*70}")
    print(f"BATCH MAE REPORT - {len(chat_results)} Chats")
    print(f"{'='*70}")
    print(f"\n{'ChatID':<15} {'MAE':>10} {'Interpretation':<40}")
    print(f"{'-'*70}")
    
    for chat_id, result in chat_results:
        print(f"{chat_id:<15} {result.mae:>10.2f} {result.interpretation:<40}")
    
    print(f"{'-'*70}")
    print(f"{'AVERAGE MAE:':<15} {avg_mae:>10.2f} {interpret_mae(avg_mae):<40}")
    print(f"{'='*70}\n")


# Example usage
if __name__ == "__main__":
    # Example 1: Single chat calculation (ChatID 27811316 from your example)
    print("EXAMPLE 1: Single Chat Evaluation")
    
    ai_scores = {
        'IssueIdentification': 4,
        'ResolutionCompliance': 3,
        'Clarity': 2,
        'Retention': 2,
        'Sentiment': 3,
        'CustomerCentricity': 4
    }
    
    human_scores = {
        'IssueIdentification': 4,
        'ResolutionCompliance': 3,
        'Clarity': 2,
        'Retention': 2,
        'Sentiment': 4,
        'CustomerCentricity': 3
    }
    
    result = calculate_mae(ai_scores, human_scores)
    print_mae_report('27811316', result, ai_scores, human_scores)
    
    # Example 2: Batch calculation
    print("\nEXAMPLE 2: Batch Evaluation")
    
    chats = [
        {
            'chat_id': '27811316',
            'ai_scores': ai_scores,
            'human_scores': human_scores
        },
        {
            'chat_id': '27811317',
            'ai_scores': {
                'IssueIdentification': 3,
                'ResolutionCompliance': 2,
                'Clarity': 3,
                'Retention': 3,
                'Sentiment': 4,
                'CustomerCentricity': 3
            },
            'human_scores': {
                'IssueIdentification': 4,
                'ResolutionCompliance': 3,
                'Clarity': 2,
                'Retention': 3,
                'Sentiment': 4,
                'CustomerCentricity': 4
            }
        }
    ]
    
    avg_mae, results = calculate_batch_mae(chats)
    chat_results = [(chat['chat_id'], result) for chat, result in zip(chats, results)]
    print_batch_report(avg_mae, chat_results)
