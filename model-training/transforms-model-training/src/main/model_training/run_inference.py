from transforms.api import transform, Input, Output
from palantir_models.transforms import ModelInput


@transform(
    inference_input=Input("/path/to/inference_input"),
    model_input=ModelInput("/path/to/model"),
    inference_output=Output("/path/to/inference_output"),
)
def compute(inference_input, model_input, inference_output):
    inference_results = model_input.transform(inference_input)
    inference_output.write_pandas(inference_results.output_df)
