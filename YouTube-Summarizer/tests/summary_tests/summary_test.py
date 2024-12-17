from rouge_score import rouge_scorer
from bert_score import score as bert_score
import json

OUTPUTFILENAME = "summary_test_results.json"


def calculate_rouge_metric(generated_summ, reference_summ, test_case_numm):
    scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)
    rouge_scores = scorer.score(reference_summ, generated_summ)
    
    print(f"TEST CASE: {test_case_numm}")
    print(f"ROUGE-1: {rouge_scores['rouge1'].fmeasure:.4f}")
    print(f"ROUGE-2: {rouge_scores['rouge2'].fmeasure:.4f}")
    print(f"ROUGE-L: {rouge_scores['rougeL'].fmeasure:.4f}")
    
def calulate_bert_metric(filename:str):
    out_data = []
    with open(filename, 'r') as file:
        data = json.load(file)
    for idx, item in enumerate(data):
        precision, recall, f1 = bert_score([item['generated_summary']], [item['reference_summary']], lang='en', verbose=True)
        print(f1.numpy()[0])
        print(precision.numpy()[0])
        print(recall.numpy()[0])
        bert_score_dict = {
            'index':idx,
            'precision':str(precision.numpy()[0]),
            'recall':str(recall.numpy()[0]),
            'f1':str(f1.numpy()[0])
        }
        out_data.append(bert_score_dict)
    with open("BERTMetricOutput.json",'w') as file:
        json.dump(out_data, file)
        
        
if __name__ == '__main__':
    calulate_bert_metric(OUTPUTFILENAME)