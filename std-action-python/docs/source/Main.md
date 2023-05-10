# Standard Python Action Template

This template gives the starting point for writing a render post-processing action. It resolves the path to the rendered images from the current configuration, loads the images and saves them as JPG.

In the module `image-render-workspace-test` there is a demo configuration that uses this post processing action. This can be found in the folder `config/tpl/pyact-01`. To use this configuration you must do the following:

1. Instantiate from the template via `cathy install template std-action-python`.
2. Install the created module in your python environment by changing to the newly created module folder and calling `pip install .` or `pip install -e .` if you want to develop the template further.
3. Have a look at the `setup.cfg` file of the create module. There is a definition `catharsys.action`. The part left of the equal sign in the definition is the action type id string, e.g. `/catharsys/action/hello/world:1.0`.
4. Use this action type id string in the `launch.json` of the `pyact-01` configuration as `sActionDTI` value for the `pyact` action.

Now you can first launch the render actions and after that has finished launch the `pyact` action, which will call the newly created action module.
