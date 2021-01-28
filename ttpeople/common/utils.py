import re
import lxml
import lxml.html.clean


def get_clearfix_text(content,
                      remove_tags=None,
                      kill_tags=None,
                      rm_repeat_symbol=True,
                      ret_str=True,
                      sep='\n\n',
                      add_root=False,
                      readable=False):
    """重构dom树，目的是为了保持原html格式

    Params:
        - content: list | str, 要抽取的原html片段
        - remove_tags: [tag1,tag2...], 将文字提取到上一级目录的标签
        - kill_tags: [tag1,tag2...], 需要移除的标签
        - rm_repeat_symbol: bool, 是否移除重复的之类的无效符号，如换行、空格等
        - ret_str: bool，返回结果是否为字符串，如果否，则返回list
        - sep: str, 连接字符串符号，一般为''、 ' '、 '\n'
        - add_root: bool, 是否添加根元素，如果content为纯文本的话会抛出异常，可以添加根元素解决。
        - readable: bool，是否可读，大部分文章已经保持了格式，所以默认为False。如果为True，将调用utils.make_readable()

    Returns:
        - list | str, 只包含纯文本内容的一个列表或字符串
    """
    if isinstance(content, list):
        content = ''.join(content)
    if add_root:
        content = f'<body>{content}</body>'

    remove_tags = remove_tags or ['a', 'b', 'em', 'strong', 'font', 'i', 'sub', 'span', 'keyword', 'sup']
    clearer = lxml.html.clean.Cleaner(
        page_structure=False,
        style=True,
        remove_tags=remove_tags,
        kill_tags=kill_tags,
        remove_unknown_tags=False
    )
    content_nobr = re.sub(r'<br\s?/?>', r'\n', content)
    html_txt = clearer.clean_html(content_nobr)
    dom = lxml.html.fromstring(html_txt)
    texts = dom.xpath('//text()')
    results = []
    if rm_repeat_symbol:
        latest_statement = ''
        for text in texts:
            txt = re.sub(r'\r?\n', r'\n', text)
            txt = re.sub(r'\t+', r'\t', txt)
            txt = re.sub(r'\n+', r'\n', txt)
            txt = re.sub(r'(\n[\t|\s+])+', sep, txt)
            curr_statement = re.sub('&nbsp;?|\xa0|&#160;?', ' ', txt)
            curr_txt = curr_statement.strip()
            if not curr_txt or curr_txt == latest_statement.strip(): continue
            latest_statement = curr_txt
            results.append(curr_statement.strip())

    if ret_str:
        content_text = sep.join(results).strip()
        return make_readable(content_text) if readable else content_text
    return results


def make_readable(text, sep='\n\n', replace=True):
    """增强可读性，与整体风格保持一致

    Params:
        - text: str, 要替换的文本
        - sep: str, 分隔符号
        - replace: bool,是否替换\n为sep

    Returns:
        - str
    """
    if replace:
        text = str(text).replace('\n', sep)
    return re.sub(r'\n{2,}', sep, text).strip()
