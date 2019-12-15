def metric(tp, tn, fp, fn):
    tot = tp + tn + fp + fn
    acc = (tp + tn)/(tp + tn + fp + fn)
    prec = tp / (tp + fp)
    rec = tp / tp + fn
    f1 = 2*tp/(2*tp+fp+fn)
    FOR = fn / (fn + tn)

    return acc,prec,rec,f1,FOR
        
