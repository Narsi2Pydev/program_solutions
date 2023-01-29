import dtlpy as dl
from datetime import timezone
import datetime
#My dataloop Credentilas
email='narsi.electrical999@gmail.com'
password = ''

def run_the_dataloop(project_name: str, dataset_name: str):
    #Login method
    if dl.token_expired():
        #dl.login()
        dl.login_m2m(email=email, password=password)
        # Get the project

    try:
        project = dl.projects.create(project_name=project_name) #create your project
    except:
        project = dl.projects.get(project_name=project_name)

    # Get the dataset
    # Get items in pages (100 item per page)

    #Creating a New DataSet
    try:
        data_set = project.datasets.create(dataset_name=dataset_name)
    except:
        #getting the created dataset
        dataset = project.datasets.get(dataset_name=dataset_name)

    #creating the Labesl
    labels = [
        dl.Label(tag='Class1', color=(255, 100, 0)),
        dl.Label(tag='Class2', color=(34, 56, 7)),
        dl.Label(tag='key', color=(100, 14, 150))
    ]

    #labels = ['Class1', 'Class2', 'key']
    dataset.add_labels(label_list=labels)

    #Createting the Recipe with labels
    try:
        recipe = dataset.recipes.create(recipe_name='My-Testing-Recipe', labels=labels)
    except Exception as exe:
        print('recipe name already existing {0}'.format(str(exe)))


    #Uploading the Data
    uploaded_items = dataset.items.upload(local_path='D:/Projects_DA/Testing') #Change your path here

    #Adding utc time to the Metadata
    utc_time = datetime.datetime.now(timezone.utc).isoformat()

    #method I to update the Metadata of the
    #Filtering the  uploaded items
    #filters = dl.Filters()
    #filters.add(field='dir', values='/Testing')
    #dataset.items.update(filters=filters, update_values={'user': {'dateTime': utc_time}})

    #method2:  one at a time

    # for item in uploaded_items:
    #     item.metadata['user'] = dict()
    #     item.metadata['user']['datetime'] = utc_time
    #     # update and reclaim item
    #     item = item.update()

    # method 2 ends here

    for count, item in enumerate(uploaded_items):
        if count < 2:
              label_name = 'Class1'
        else:
              label_name = 'Class2'
        item.label = label_name # clasifying the item
        item.metadata['user'] = dict()
        item.metadata['user']['datetime'] = utc_time  # Adding meta Data Field
        item.update()
        builder = item.annotations.builder() # ading the aanotations to item
        builder.add(annotation_definition=dl.Classification(label=label_name))
        item.annotations.upload(builder)

    # Query to filter the Class1 labeled items
    class_filter = dl.Filters()
    class1_filter = class_filter.add(field='label', values='Class1')
    item_Class1 = dataset.items.list(filters=class1_filter)

    # class_filter = dl.Filters(resource=dl.FILTERS_RESOURCE_ITEM)
    # class1_filter = person_filter.add(field='label', values='Class1')
    # #dataset.add_label(label_name='Class1')
    # pages = dataset.items.list(filters=class1_filter)

    # Count the items

    # Getting the All point Annotations Datasets
    annotations =  dataset.annotations.list()
    for annotation in annotations:
        annotation.print()


if __name__ == '__main__':
    project_name = 'Sports Events'
    dataset_name = 'My-Testing-Dataset'
    run_the_dataloop(project_name, dataset_name)
