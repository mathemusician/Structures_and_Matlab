function result = return_pde(vert_add)

% add volume constraint

if sum(vert_add) > 20
    result = 1;
    return
end

% Write vertices points
fileID = fopen('/Users/jvkyleeclarin/Desktop/vertices.txt','w');
fprintf(fileID,'%10.10e ', vert_add);
fclose(fileID);

% change stl
command = strcat('cd /Applications/blender-2.79-rc2-macOS-10.6/blender.app/Contents/MacOS/; ', ...
    ' ./blender /Users/jvkyleeclarin/Desktop/test.blend --background --python ', ...
    ' /Users/jvkyleeclarin/Desktop/change_stl.py');
system(command);

% remake stl
model = createpde('structural','static-solid');
command = 'python /Users/jvkyleeclarin/Desktop/change_stl.py change_stl';
% run this if you get into trouble
% [status,cmdout] = system(command);
system(command);

importGeometry(model,'/Users/jvkyleeclarin/Desktop/new_stl_file.stl');


structuralProperties(model,'Cell',1,'YoungsModulus',200e7, ...
                                    'PoissonsRatio',0.3);

% find the bottom and top faces
[p,e,~] = model.generateMesh.meshToPet();
% get highest z_axis number
highest_number = max(p(3,:));
% get lowest z_axis number
lowest_number = min(p(3,:));
% account for error in stl
highest_number =  round(highest_number, 5);
lowest_number = round(lowest_number, 5);
% initialize points
z_points = p(3,:);
z_points = round(z_points, 5);
% cycle through all faces
boundary_faces = [];
load_faces = [];
% cycle through all faces
for number = 1:model.Geometry.NumFaces
    % get points in each face
    index_points = e.getElementFaces(number);
    index_points = index_points(:);
    points_in_faces = z_points(index_points);
    % account for error in stl preparation
    if all(points_in_faces == lowest_number, 1)
        % structuralBC(model,'Face',number,'Constraint','fixed');
        boundary_faces(end + 1) =  number;
    end
    if all(points_in_faces == highest_number, 1)
        % structuralBoundaryLoad(model,'Face',load_faces,'SurfaceTraction',[0,0,-distributedLoad]);
        load_faces(end + 1) = number;
    end
end

structuralBC(model,'Face',boundary_faces,'Constraint','fixed');

distributedLoad = 1e8; % Applied load in Pascals
%structuralBoundaryLoad(model,'Face',load_faces,'SurfaceTraction',[0,0,-distributedLoad]);
structuralBoundaryLoad(model,'Face',load_faces,'SurfaceTraction',[0,0,-distributedLoad]);


bracketThickness = 1e-2; % Thickness of horizontal plate with hole, meters
generateMesh(model,'Hmin',bracketThickness);

result = solve(model);
% made this purposefully negative to make optimize the minimum displacement
%figure(2)
%pdeplot3D(model,'ColorMapData',result.Displacement.uz)
result = -1*min(result.Displacement.uz);



end
