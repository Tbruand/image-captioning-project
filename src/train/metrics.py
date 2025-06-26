from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from rouge_score import rouge_scorer

# ⚙️ BLEU-3 (trigrammes)
def compute_bleu(references, hypotheses, n=3):
    smoothie = SmoothingFunction().method4
    scores = []
    for ref, hyp in zip(references, hypotheses):
        ref_tokens = ref.lower().split()
        hyp_tokens = hyp.lower().split()
        weights = tuple((1. / n for _ in range(n)))
        score = sentence_bleu([ref_tokens], hyp_tokens, weights=weights, smoothing_function=smoothie)
        scores.append(score)
    return sum(scores) / len(scores)

# ⚙️ ROUGE-L
def compute_rouge(references, hypotheses):
    scorer = rouge_scorer.RougeScorer(['rougeL'], use_stemmer=True)
    scores = []
    for ref, hyp in zip(references, hypotheses):
        score = scorer.score(ref, hyp)['rougeL'].fmeasure
        scores.append(score)
    return sum(scores) / len(scores)