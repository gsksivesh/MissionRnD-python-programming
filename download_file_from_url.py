import urllib2
import click


@click.command()
@click.option('--url', prompt='Enter URL',
              help='The URL to download.')
def download(url):
    try:
        response = urllib2.urlopen(url)
    except Exception, e:
        click.echo(e)
        return
    info=response.info()
    is_html = "text/html" in info.getheaders('Content-Type')[0]
    if is_html:
        click.echo("Url doesn't contain file.")
        return
    file_name=url.split('/')[-1]
    with open(file_name, 'wb') as output:
        while True:
            data = response.read(4096)
            if data:
                output.write(data)
            else:
                break
    click.echo("Successfully Downloaded")

if __name__ == '__main__':
    download()
