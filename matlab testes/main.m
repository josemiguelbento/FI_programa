close all
clear
clc

% Determine where your m-file's folder is.
folder = fileparts(which(mfilename)); 
% Add that folder plus all subfolders to the path.
addpath(genpath(folder));

data_functions = leitura_dados; %defining class data

%user defined
%data_file_date = input('Please input the date of the file (Eg: 06_11_2021): ', 's');
file_folder = "asteroids";
%file_name = input('Please input the name of the file (Eg: 2008ev5.txt): ','s');
file_name = "2008ev5.txt";

%view = input("Do you want to see the plots? 1 if yes and 0 if no: ");
%save = input("Do you want to save the plots? 1 if yes and 0 if no: ");
%get data from the file
% try
[index, data_x, data_y, data_z] = data_functions.GET_DATA(file_folder, file_name);

j = 1;
k = 1;
for i = 1:length(index)
    if index(i) == 'v'
        vol_x(j,1) = data_x(i);
        vol_y(j,1) = data_y(i);
        vol_z(j,1) = data_z(i);
        j = j+1;
    end
    if index(i) == 'f'
        f_x(k,1) = data_x(i);
        f_y(k,1) = data_y(i);
        f_z(k,1) = data_z(i);
        k = k+1;
    end
end
figure(1)
plot3(vol_x,vol_y,vol_z, '.')
figure(2)
plot3(f_x,f_y,f_z, '.')

% figure(3)
% xi = unique(vol_x) ; yi = unique(vol_y) ;
% [X,Y] = meshgrid(xi, yi);
% Z = reshape(vol_z,size(X)) ;
% surf(X,Y,Z)

%unstructured 
dt = delaunayTriangulation(vol_x,vol_y) ;
tri = dt.ConnectivityList ;
figure(4)
trisurf(tri,vol_x,vol_y,vol_z)

% figure(5)
% stem3(vol_x, vol_y, vol_z)
% grid on
% xv = linspace(min(vol_x), max(vol_x), 20);
% yv = linspace(min(vol_y), max(vol_y), 20);
% [X,Y] = meshgrid(xv, yv);
% Z = griddata(vol_x,vol_y,vol_z,X,Y);
% 
% figure(6)
% surf(X, Y, Z);
% grid on
% set(gca, 'ZLim',[0 100])
% shading interp