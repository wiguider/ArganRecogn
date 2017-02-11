# this class has aim to use the neural net after trainning
# see doc : https://turi.com/learn/userguide/supervised-learning/neuralnet-classifier.html
# TODO: read doc and appliquer
import graphlab as gl


class NetEval:
    test_data = None
    data = None

    def init(self, test, train):
        self.test_data = test
        self.data = train

    def test(self):
        net_string = file('MyNet').read()
        net2 = gl.deeplearning.loads(net_string)
        model = gl.neuralnet_classifier.create(self.data, target='Class', network=net2)
        # Classify test data and evaluate the model
        pred = model.classify(self.test_data)
        print pred
        results = model.evaluate(self.test_data)
        print results
