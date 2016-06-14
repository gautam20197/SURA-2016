function p = predict(Theta1, Theta2, X)
%PREDICT Predict the label of an input given a trained neural network
%   p = PREDICT(Theta1, Theta2, X) outputs the predicted label of X given the
%   trained weights of a neural network (Theta1, Theta2)

% Useful values
m = size(X, 1);
X=[ones(m,1) X];
act1=X*(Theta1');
act=sigmoid(act1);
act=[ones(m,1) act];
z3=act*(Theta2');
p=sigmoid(act*(Theta2'));

% =========================================================================


end