#pragma include Shaders/base

void main(){
    gl_Position = p3d_ModelViewProjectionMatrix * p3d_Vertex * sin(osg_FrameTime);
}