
__all__ = ['post_modules']

def register(module, paras, args):
    for p in module.__all__:
        paras.append(p)
        args.append(module.__dict__.get(p))

def get_lib_env():
    paras, args = [], []
    from post_libs import post_functions
    register(post_functions, paras, args)

    return dict(zip(paras, args))

post_modules = get_lib_env()
