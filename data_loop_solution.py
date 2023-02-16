import dtlpy as dl
from datetime import timezone
import datetime
#My dataloop Credentilas
email='narsi.electrical999@gmail.com'
password = ''

def run_the_dataloop(project_name: str, dataset_name: str, random_points=[]):
    #Login method
    if dl.token_expired():
        #dl.login()
        dl.login_m2m(email=email, password=password)
        # Get the project
    #project = dl.projects.get(project_name='My_Dummy_Proj')
    try:
        project = dl.projects.get(project_name=project_name)
         #create your project
    except:
        project = dl.projects.create(project_name=project_name)


    # Get the dataset
    # Get items in pages (100 item per page)

    #Creating a New DataSet
    try:
        # getting the created dataset
        dataset = project.datasets.get(dataset_name=dataset_name)
    except:
        data_set = project.datasets.create(dataset_name=dataset_name)


    #creating the Labesl
    labels = [
        dl.Label(tag='Class1', color=(255, 100, 0)),
        dl.Label(tag='Class2', color=(34, 56, 7)),
        dl.Label(tag='Key', color=(100, 14, 150))
    ]

    #labels = ['Class1', 'Class2', 'key']
    dataset.add_labels(label_list=labels)

    #Commented the Receipe Creation
    #Createting the Recipe with labels #Commented it for not needed
    # try:
    #     recipe = dataset.recipes.create(recipe_name='My-Testing-Recipe', labels=labels)
    # except Exception as exe:
    #     print('recipe name already existing {0}'.format(str(exe)))


    #Uploading the Data
    uploaded_items = dataset.items.upload(local_path='D:/Projects_DA/Testing') #Change your path here
    uploaded_items_list = list(uploaded_items)
    #Adding utc time to the Metadata
    utc_time = datetime.datetime.now(timezone.utc).isoformat()

    #Method one
    Updating the all the metadata at once
    Filtering the  uploaded items
    filters = dl.Filters()
    filters.add(field='dir', values='/Testing')
    dataset.items.update(filters=filters, update_values={'user': {'utc_dateTime': utc_time}})

    #method2:  Updating the metadata field one at a time

    # for item in uploaded_items_list:
    #     item.metadata['user'] = dict()
    #     item.metadata['user']['utc_datetime'] = utc_time
    #     # update and reclaim item
    #     item = item.update()

    # method 2 ends here

    for count, item in enumerate(uploaded_items_list):
        if count < 2:
              label_name = 'Class1'
        else:
              label_name = 'Class2'
        builder = item.annotations.builder()  # ading the aanotations to item

        if count+1 == len(uploaded_items_list):  #Adding 5 random key points
            for random_point in random_points:
                builder.add(annotation_definition=dl.Point(x=random_point[0], y=random_point[1], label='Key'))
            #builder.add(annotation_definition=dl.Classification(label=label_name)) #this optional clasicfication of same item as claas2
        else:
            builder.add(annotation_definition=dl.Classification(label=label_name))
        item.annotations.upload(builder)

    # First filter to filter the Class1 labeled items
    #class1_filter = dl.Filters(resource='annotations',field='label', values = 'Class1')
    class1_filter = dl.Filters()
    class1_filter.add_join(field='label', values = 'Class1')
    item_Class1 = dataset.items.list(filters=class1_filter)
    for item_cls1 in item_Class1:
        item_cls1.print()

    # Getting the All point Annotations of Datasets second filter
    annotations = dataset.annotations.list(filters=dl.Filters(resource=dl.FiltersResource.ANNOTATION).add(field='label', values=['Class1','Class2','Key']))
    #annotations =  dataset.annotations.list()
    for annotation in annotations:
        annotation.print()

if __name__ == '__main__':
    project_name = 'Sports Events'
    dataset_name = 'My-Testing-Dataset'
    run_the_dataloop(project_name, dataset_name, random_points=[(50,50), (10,10),(20,20), (30,30), (40,40)] )

