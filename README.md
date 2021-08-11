# Deregister AMIs older than a custom age that matches a given name filter
This GitHub Action allows users to remove older AWS AMI versions, avoid messy accounts and incurring costs. In order to used this feature you'll specify the search string and owner to find matching AMIs. Then, images older than `max_age` days will be removed. Additionally, you can set a deprecation date on the other AMIs found but are yet too young.  

## Usage

The easiest way of using this action is to authenticate using [AWS Official Credentials Setup](https://github.com/marketplace/actions/configure-aws-credentials-action-for-github-actions) and them calling this action:

```yaml
on:
  workflow_dispatch: # manual dispatch is also possible!
  schedule:
    - cron: '07 18 30 * *' # https://crontab.guru/
name: Remove AMIs older than 90 days
jobs:
  pre-job:
    runs-on: ubuntu-latest
    steps:
    - name: Configure AWS Credentials
      uses: aws-actions/configure-aws-credentials@v1
      with:
        aws-access-key-id: ${{ secrets.AWS_ACCESS_ID }}
        aws-secret-access-key: ${{ secrets.AWS_SECRET_KEY }}
        aws-region: ${{ secrets.AWS_DEFAULT_REGION }}
      - uses: PasseiDireto/deregister-aws-ami-action@main
        with:
          name_filter: 'image-name-dev*'
          max_age: 60 # in days
          owner: ${{ secrets.OWNER_ID }}
          set_deprecation_date: true

```

The most common use case is to schedule this action to run periodically, allowing a constant cleanse of older AMIs. The default behavior is to enable a deprecation date on AMIs that were found but are too young yet. In this case, the deprecation date will be calculated based on the AMI creation date plus the defined `max_age` (in days). You can disable this feature setting `set_deprecation_date` as `false`. 

## Contributing

PRs welcome! This action is a Docker container, so it is very easy run it locally. Be sure you have all the required inputs represented as envrionment variables. For instance you will need a `INPUT_NAME_FILTER` to represent the input `name_filter` the action will actually pass. Note the `INPUT_` preffix and the camel case representation.

### Development guide
Be sure you have Python 3.9, otherwise Make won't run as it should. An easy solution is to run `make` commands inside a Docker container.

Clone the repository using Git:
```shell script
git clone git@github.com:PasseiDireto/deregister-aws-amis-action.git
```

You can build the image as:

```shell script
docker build -t deregister-aws-amis-action .
```

Have an [env file](https://docs.docker.com/engine/reference/commandline/run/#set-environment-variables--e---env---env-file) ready with all the variables you need, such as:

```shell script


```

You can name it `.env` and then run it the freshly built image:

```shell script
docker run --rm --env-file=.env deregister-aws-amis-action
```


### Before you commit

Be sure all the tests and all the checks are passing:
```sh
pip install -r requirements/all.txt
make # run all checks
make tests # run all tests

```