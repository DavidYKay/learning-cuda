"""
SCons.Tool.cuda

CUDA Tool for SCons

"""

import os
import sys
import SCons.Tool
import SCons.Scanner.C
import SCons.Defaults

CUDAScanner = SCons.Scanner.C.CScanner()

def CUDANVCCStaticObjectEmitter(target, source, env):
    tgt, src = SCons.Defaults.StaticObjectEmitter(target, source, env)
    for f in tgt:
        lifile = os.path.splitext(f.rstr())[0] + '.linkinfo'
        env.SideEffect(lifile, f)
        env.Clean(f, lifile)
    return tgt, src

def CUDANVCCSharedObjectEmitter(target, source, env):
    tgt, src = SCons.Defaults.SharedObjectEmitter(target, source, env)
    for f in tgt:
        lifile = os.path.splitext(f.rstr())[0] + '.linkinfo'
        env.SideEffect(lifile, f )
        env.Clean(f, lifile )
    return tgt, src

def generate(env):
    staticObjBuilder, sharedObjBuilder = SCons.Tool.createObjBuilders(env)
    staticObjBuilder.add_action('.cu', '$STATICNVCCCMD')
    staticObjBuilder.add_emitter('.cu', CUDANVCCStaticObjectEmitter)
    sharedObjBuilder.add_action('.cu', '$SHAREDNVCCCMD')
    sharedObjBuilder.add_emitter('.cu', CUDANVCCSharedObjectEmitter)
    SCons.Tool.SourceFileScanner.add_scanner('.cu', CUDAScanner)

    # default compiler
    env['NVCC'] = 'nvcc'

    # default flags for the NVCC compiler
    env['NVCCFLAGS'] = ''
    env['STATICNVCCFLAGS'] = ''
    env['SHAREDNVCCFLAGS'] = ''
    env['ENABLESHAREDNVCCFLAG'] = '-shared'

    # default NVCC commands
    env['STATICNVCCCMD'] = '$NVCC -o $TARGET -c $NVCCFLAGS $STATICNVCCFLAGS $SOURCES'
    env['SHAREDNVCCCMD'] = '$NVCC -o $TARGET -c $NVCCFLAGS $SHAREDNVCCFLAGS $ENABLESHAREDNVCCFLAG $SOURCES'

    cudaToolkitPath = '/usr/local/cuda'
    env['CUDA_TOOLKIT_PATH'] = cudaToolkitPath
    #env['CUDA_SDK_PATH'] = cudaSDKPath

    platform = 'x86_64-linux'

    # add nvcc to PATH
    env.PrependENVPath('PATH', cudaToolkitPath + '/bin')

    # add required libraries
    env.Append(CPPPATH=[cudaToolkitPath + '/samples/common/inc',
                        cudaToolkitPath + 'include',
                        cudaToolkitPath + '/targets/%s/include' % platform,])

    env.Append(LIBPATH=[cudaToolkitPath + '/samples/common/lib',
                        cudaToolkitPath + '/targets/%s/lib' % platform,])
    env.Append(LIBS=['cudart'])
    env.Append(RPATH = cudaToolkitPath + 'targets/%s/lib' % platform)
    
def exists(env):
    return env.Detect('nvcc')
