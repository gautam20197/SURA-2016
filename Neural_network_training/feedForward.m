function p = feedForward(Theta1, Theta2, Theta3, X)
m = size(X, 1);
X=[ones(m,1) X];
act1=sigmoid(X*(Theta1'));
act1=[ones(size(act1,1),1) act1];
act2=sigmoid(act1*(Theta2'));
act2=[ones(size(act2,1),1) act2];
p=sigmoid(act2*(Theta3'));

% =========================================================================


end
