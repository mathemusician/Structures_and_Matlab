% This is the main function
% Dependencies: return_pde.m
%               change_stl.py
%               test.blend


% initialize function
FitnessFunction = @return_pde;
numberOfVariables = 51;
opts = optimoptions(@ga,'PlotFcn',{@gaplotbestf,@gaplotstopping});

% maximum stall generations to 100.
opts = optimoptions(opts,'MaxGenerations',20,'MaxStallGenerations', 30, ...
                    'CreationFcn',@gacreationuniform);
%%
% Run the |ga| solver.

% lower and upper bound
lb = zeros(1, 51);
ub = lb + 1;
% execute solver
[x,Fval,exitFlag,Output] = ga(FitnessFunction,numberOfVariables,[],[],[],[], ...
    lb,ub,[],opts);

fprintf('The number of generations was : %d\n', Output.generations);
fprintf('The number of function evaluations was : %d\n', Output.funccount);
fprintf('The best function value found was : %g\n', Fval);
