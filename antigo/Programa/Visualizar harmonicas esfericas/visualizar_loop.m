close all
clc
clear all
n=50;
phi=linspace(0,2*pi,n);
theta=linspace(0,pi,n);

[PHI, THETA]=meshgrid(phi,theta);
j=0;
for l = 0:3
    for m = 0:l
        j = j+1
        a=sqrt(((2*l+1)/(4*pi))*(((factorial(l-m))/(factorial(l+m)))));
        syms s;
        
        M=[(s^2-1)^l];
        G(s)=M;
        N=[(1-s^2)^(m/2)];
        H(s)=N;
        P_ml(s)=((-1)^m/(factorial(l)*(2^l)))*H(s)*diff(G(s),l+m);
        
        
        
        %Com l par, quando R=imag(R), o resultado é zero. mas com l impar
        %o resultado é a sobreposição de R real e R imag
        
        
        
        R=a.*exp(1i*m*PHI).*double(P_ml(cos(THETA)));
        R1=abs(real(R));
        R2=abs(imag(R));
        
        
        x1 = R1 .* sin(THETA) .* cos(PHI);
        y1 = R1.* sin(THETA) .* sin(PHI);
        z1 = R1 .* cos(THETA);
        
        figure(j)
        surf(x1,y1,z1);
        title(strcat("l = ", num2str(l), "    m = ", num2str(m)));
    end
end






 

