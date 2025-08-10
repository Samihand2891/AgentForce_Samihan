import json
from schema import AcademicPlan
from pydantic import ValidationError
def generate_academic_plan(user_goal: str, pipeline_instance):
    json_schema = AcademicPlan.model_json_schema()
    prompt= f"""<start_of_turn>user 
    You are an user expert academic and career advisor for University Students in tech , Management.
    A student has the following goal: "{user_goal}".
    
    Generate a detailed, semester by semester academic plan with detailed steps to help them achieve this goal. 
    The output MUST be a JSON object that strictly conforms to the following JSON Schema. 
    Do not include any text or explanation outside of JSON object. 

    JSON Schema: 
    {json.dumps(json_schema, indent=2)} <end_of_turn>
    <start_of_turn>model
    """
    outputs = pipeline_instance(prompt,
    max_new_tokens=8192,
    do_sample=True,
    temperature=0.7,
    top_k=50,
    top_p=0.95,)
    response_text = outputs["generated_text"]
    try: 
        json_start = response_text.find('{') 
        json_end = response_text.rfind('}') + 1
        if json_start == -1 or json_end == 0:
            raise ValueError("No JSON object found in the model's response.")
        json_string = response_text[json_start:json_end]
        
        parsed_output = AcademicPlan.model_validate_json(json_string)
        return parsed_output
    except (json.JSONDecodeError, ValidationError, ValueError) as e:
        print(f"error parsing model output: {e}")
        print(f"RawresponseModel: {response_text}")
        return None 



