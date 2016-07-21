
def makeFiguretype_OneParamAndRepetitions_Accuracy(params, paramString):
	import figuretype_OneParamAndRepetitions_Accuracy
	print "Making figure type OneParamAndRepetitions_Accuracy(..) for parameter '"+paramString+"'."
	figuretype_OneParamAndRepetitions_Accuracy.makeFig(params, paramString)


def makeFigureType_FinalWeightsWithRepetitions(params):
	import repetitionsummary
	print "Making figure type FinalWeightsWithRepetitions for all parameters."
	repetitionsummary.make_repetitionsummary_figures(params)


def makeFigureType_DevelopmentOfResponses(params):
	import repetitiondetail
	print "Making figure type DevelopmentOfResponses for all parameters."
	repetitiondetail.make_singlerun_figures(params)

