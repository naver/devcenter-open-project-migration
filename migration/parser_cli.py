import click


@click.command()
@click.option('--project_name', type=str, help='nFORGE 프로젝트 이름', prompt=True)
@click.option('--dev_code', type=str, help='DevCode 유무', is_flag=True, default=False)
def parser_cli(project_name, dev_code):
    # 폴더 만들기
    pass


if __name__ == '__main__':
    parser_cli()
