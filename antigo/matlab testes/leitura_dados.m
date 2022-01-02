classdef leitura_dados
    methods
        function [index, data_x, data_y, data_z]= GET_DATA(obj,file_folder, file_name)
            
            filedir = string(split(mfilename('fullpath'), '\leitura_dados')); %get file folder

            %go into the data file folder
            data_file_dir = strcat(filedir(1), '\data\', file_folder);
            cd (data_file_dir);
            file = strcat(filedir(1), '\data\', file_folder, "\", file_name);
            data_file_id = fopen(file,'r');
            DATAO = textscan(data_file_id, '%c %f %f %f', 'Delimiter', ' ','TreatAsEmpty','~');
            %DATAO = fscanf(data_dile_id,'%*s = %f');
            fclose(data_file_id);
            index = char(DATAO(1,1));
            DATAO = DATAO(1,2:length(DATAO));
            
            readings = cell2mat(DATAO);
            data_x = readings(:,1);
            data_y = readings(:,2);
            data_z = readings(:,3);
        end
    end
end