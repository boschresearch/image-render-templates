# Blender Modifier Template

This is a template for a Blender modifier that can be referenced via a Blender modification configuration. See `image-render-workspace-examples/config/modifier` for the set of all modifiers, ordered by type, that already exist. 
This example, uses an object modifier to demonstrate the minimal setup. 

Install this template with the command:

    cathy install template std-modifier-blender

This call will ask you a couple of questions, regarding the names of the module, the namespace and the name of the modifier. You can later add any number of modifiers to this template.

## The Entry Point Definition

In the file `setup.cfg` under `[options.entry_points]`, Catharsys entry points can be listed. The example modifier in this template acts on a single object, so it is listed in the entry point group `catharsys.beldner.modify`. To see all the available groups for blender modifiers, have a look at

    image-render-actions-std-blender/setup.cfg

Each entry point has the form `[name]=[python module]:[function name]`. For Catharsys modifiers the name must have the structure of a data type information (DTI) string. In particular, for an object modifier, the first part of the DTI string must be `/catharsys/blender/modify/object/`. You can then add any additional nesting after this, for example,
`/catharsys/blender/modify/object/my-modifiers/location:1.0`. You can use the version number to keep your modifiers backwards compatible, while also offering new versions with possible breaking changes. The convention is that higher minor versions must be backward compatible to lower minor versions for the same major versions, e.g. 1.3 must be compatible with 1.0. However, different major version can have breaking changes. 

In the entry point list you can reference different python functions for different versions of the same modifier base name. 

## The Actual Modifier

The actual modifier code is located in `src/catharsys/plugins/_ext_/blender/modify/func/example.py`, to keep it in line with the namespace of the standard Blender modifiers. The `_ext_` and `example` names are replaced by the names you specify during instantiation of the template. You do not need to use this structure and you can also define any number of modifiers in any number of files. The template just defines the bare minimum needed.

## The Configuration

In the `config` folder you find an example configuration file to call the modifier. In this example, the modifier will be applied to the object with the name `Cube`.

