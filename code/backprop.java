public class Backprop {
  public static void backprop(double[][] weights, double[] inputs, double[] targets, double learningRate) {
    int numInputs = inputs.length;
    int numOutputs = targets.length;
    
    // Calculate output layer activations
    double[] outputs = new double[numOutputs];
    for (int i = 0; i < numOutputs; i++) {
      outputs[i] = sigmoid(dotProduct(weights[0], inputs));
    }
    
    // Calculate error for output layer
    double[] outputErrors = new double[numOutputs];
    for (int i = 0; i < numOutputs; i++) {
      outputErrors[i] = targets[i] - outputs[i];
    }
    
    // Calculate gradients for output layer weights
    double[][] outputGradients = new double[1][numInputs];
    for (int i = 0; i < numInputs; i++) {
      outputGradients[0][i] = outputErrors[0] * sigmoidDerivative(outputs[0]) * inputs[i];
    }
    
    // Update weights
    for (int i = 0; i < numInputs; i++) {
      weights[0][i] += learningRate * outputGradients[0][i];
    }
  }
  
  private static double sigmoid(double x) {
    return 1 / (1 + Math.exp(-x));
  }
  
  private static double sigmoidDerivative(double x) {
    return x * (1 - x);
  }
  
  private static double dotProduct(double[] a, double[] b) {
    double sum = 0;
    for (int i = 0; i < a.length; i++) {
      sum += a[i] * b[i];
    }
    return sum;
  }
}