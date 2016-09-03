
clear ; close all; clc                                

fprintf('Loading Data ...\n')

data = load('data.txt');
X = data(:,1:8);
y = data(:,9);
m = size(X, 1);

net=network;
net.numInputs=1;
net.numLayers=3;
net.biasConnect(1)=1;
net.biasConnect(2)=1;
net.biasConnect(3)=1;
net.inputConnect=[1;0;0];
net.layerConnect=[0,0,0;1,0,0;0,1,0];
net.outputConnect=[0 0 1];
net.inputs{1}.size=8;
net.layers{1}.size=8;
net.layers{1}.transferFcn='logsig';
net.layers{1}.initFcn = 'initnw';
net.layers{2}.size=3;
net.layers{2}.transferFcn='logsig';
net.layers{2}.initFcn='initnw';
net.layers{3}.size=1;
net.layers{3}.transferFcn='logsig';
net.layers{3}.initFcn='initnw';
net.trainFcn = 'trainlm';
net.divideFcn='dividerand';
net.divideParam.trainRatio=85/100;
net.divideParam.valRatio=15/100;
net.divideParam.testRatio=0/100;
net.plotFcns = {'plotperform','plottrainstate'};
net=init(net);
net=train(net,X',y');
Theta1=[net.b{1}, net.IW{1,1}];
Theta2=[net.b{2}, net.LW{2,1}];
Theta3=[net.b{3}, net.LW{3,2}];
pred=feedForward(Theta1,Theta2,Theta3,X);

fprintf('\nTraining Set Accuracy: %f\n', mean(double(abs(pred-y)<0.05)) * 100);



%x1_vals=linspace(0,1,100);
%x2_vals=linspace(0,1,100);
%y_vals = zeros(length(x1_vals), length(x2_vals));

%for i = 1:length(x1_vals)
 %   for j = 1:length(x2_vals)
%	  y_vals(i,j) = predict(Theta1,Theta2,[x1_vals(i) x2_vals(j)]);
 %   end
%end

%y_vals = y_vals';
% Surface plot
%figure;
%surf(x1_vals, x2_vals, y_vals)
%xlabel('Cohesion Factor'); ylabel('Readability factor');


dlmwrite('Theta1.txt',Theta1);
dlmwrite('Theta2.txt',Theta2);
dlmwrite('Theta3.txt',Theta3);

