from numba.misc.dump_style import NumbaIRLexer #TODO: Remove pending PR: https://github.com/pygments/pygments/pull/2433

def hllines(code, style):
    try:
        from pygments import highlight
        from pygments.lexers import PythonLexer
        from pygments.formatters import HtmlFormatter
    except ImportError:
        raise ImportError("please install the 'pygments' package")
    pylex = PythonLexer()
    hf = HtmlFormatter(noclasses=True, style=style, nowrap=True)
    res = highlight(code, pylex, hf)
    return res.splitlines()


def htlines(code, style):
    try:
        from pygments import highlight
        from pygments.lexers import PythonLexer
        from pygments.formatters import TerminalFormatter
    except ImportError:
        raise ImportError("please install the 'pygments' package")
    pylex = PythonLexer()
    hf = TerminalFormatter(style=style)
    res = highlight(code, pylex, hf)
    return res.splitlines()

def hllines_ir(code, style):
    try:
        from pygments import highlight
        from pygments.formatters import HtmlFormatter
    except ImportError:
        raise ImportError("please install the 'pygments' package")
    irlex = NumbaIRLexer()
    hf = HtmlFormatter(noclasses=True, style=style, nowrap=True)
    res = highlight(code, irlex, hf)
    hl_lines = res.splitlines()
    return hl_lines

def htlines_ir(code, style):
    try:
        from pygments import highlight
        from pygments.formatters import TerminalFormatter
    except ImportError:
        raise ImportError("please install the 'pygments' package")
    irlex = NumbaIRLexer()
    hf = TerminalFormatter(style=style)
    res = highlight(code, irlex, hf)
    hl_lines = res.splitlines()
    return hl_lines

def hllines_ptx(code, style):
    try:
        from pygments import highlight
        from pygments.formatters import HtmlFormatter
        from pygments.lexers.ptx import PtxLexer
    except ImportError:
        raise ImportError("please install the 'pygments' package")
    irlex = PtxLexer()
    hf = HtmlFormatter(noclasses=True, style=style, nowrap=True)
    res = highlight(code, irlex, hf)
    hl_lines = res.splitlines()
    return hl_lines

def htlines_ptx(code, style):
    try:
        from pygments import highlight
        from pygments.formatters import TerminalFormatter
        from pygments.lexers.ptx import PtxLexer
    except ImportError:
        raise ImportError("please install the 'pygments' package")
    irlex = PtxLexer()
    hf = TerminalFormatter(style=style)
    res = highlight(code, irlex, hf)
    hl_lines = res.splitlines()
    return hl_lines

def get_html_template():
    try:
        from jinja2 import Template
    except ImportError:
        raise ImportError("please install the 'jinja2' package")
    return Template("""
    <html>
    <head>
        <style>

            .annotation_table {
                color: #000000;
                font-family: italic;
                margin: 5px;
                width: 100%;
            }

            /* override JupyterLab style */
            .annotation_table td {
                text-align: left;
                background-color: white; /*Might change: transparent*/
                padding: 1px;
            }

            .annotation_table tbody tr:nth-child(even) {
                background: white;
            }

            .annotation_table code
            {
                background-color: white; /*Might change: transparent*/
                white-space: normal;
                font-size: large;
                font-style: italics;
            }

            /* End override JupyterLab style */

            tr:hover {
                background-color: rgba(92, 200, 249, 0.25);
            }

            td.object_tag summary ,
            td.lifted_tag summary{
                font-weight: bold;
                display: list-item;
            }

            span.lifted_tag {
                color: #00cc33;
            }

            span.object_tag {
                color: #cc3300;
            }


            td.lifted_tag {
                background-color: #cdf7d8;
            }

            td.object_tag {
                background-color: #fef5c8;
            }

            code.ir_code {
                color: white;
                font-style: italic;
            }

            .metadata {
                border-bottom: medium solid blue;
                display: inline-block;
                padding: 5px;
                width: 100%;
            }

            .annotations {
                padding: 5px;
            }

            .hidden {
                display: none;
            }

            .buttons {
                padding: 10px;
                cursor: pointer;
            }
        </style>
    </head>

    <body>
        {% for func_key in func_data.keys() %}
            <div class="metadata">
            Function name: {{func_data[func_key]['funcname']}}<br />
            {% if func_data[func_key]['filename'] %}
                in file: {{func_data[func_key]['filename']|escape}}<br />
            {% endif %}
            with signature: {{func_key[1]|e}}
            </div>
            <div class="annotations">
            <table class="annotation_table tex2jax_ignore">
                {%- for num, line, hl, hc in func_data[func_key]['pygments_lines'] -%}
                    {%- if func_data[func_key]['ir_lines'][num] %}
                        <tr><td style="text-align:left;" class="{{func_data[func_key]['python_tags'][num]}}">
                            <details>
                                <summary>
                                    <code>
                                    {{func_data[func_key]['N'] % num}}:
                                    {{'&nbsp;'*func_data[func_key]['python_indent'][num]}}{{hl}}
                                    </code>
                                </summary>
                                <table class="annotation_table">
                                    <tbody>
                                        {%- for ir_num, ir_lines, ir_hl, ir_hc in func_data[func_key]['pygments_ir_lines_'+num|string] %}
                                            <tr class="ir_code">
                                                <td style="text-align: left;">
                                                    <code>
                                                        {{'&nbsp;'*func_data[func_key]['ir_indent'][num][ir_num-1]}}{{ir_hl}}
                                                    </code>
                                                </td>
                                            </tr>
                                        {%- endfor -%}
                                    </tbody>
                                </table>
                            </details>
                        </td></tr>
                    {% else -%}
                        <tr><td style="text-align:left;" class="{{func_data[func_key]['python_tags'][num]}}">
                            <code>
                                {{func_data[func_key]['N'] % num}}:
                                {{'&nbsp;'*func_data[func_key]['python_indent'][num]}}{{hl}}
                            </code>
                        </td></tr>
                    {%- endif -%}
                {%- endfor -%}
            </table>
            </div>
        {% endfor %}
    </body>
    </html>
    """)

def get_html_template2():
    try:
        from jinja2 import Template
    except ImportError:
        raise ImportError("please install the 'jinja2' package")
    return Template("""
    <html>
    <head>
        <style>

            .annotation_table {
                color: #000000;
                font-family: italic;
                margin: 5px;
                width: 100%;
            }

            /* override JupyterLab style */
            .annotation_table td {
                text-align: left;
                background-color: white; /*Might change: transparent*/
                padding: 1px;
            }

            .annotation_table tbody tr:nth-child(even) {
                background: white;
            }

            .annotation_table code
            {
                background-color: white; /*Might change: transparent*/
                white-space: normal;
                font-size: large;
                font-style: italics;
            }

            /* End override JupyterLab style */

            tr:hover {
                background-color: rgba(92, 200, 249, 0.25);
            }

            td.object_tag summary ,
            td.lifted_tag summary{
                font-weight: bold;
                display: list-item;
            }

            span.lifted_tag {
                color: #00cc33;
            }

            span.object_tag {
                color: #cc3300;
            }


            td.lifted_tag {
                background-color: #cdf7d8;
            }

            td.object_tag {
                background-color: #fef5c8;
            }

            code.ir_code {
                color: white;
                font-style: italic;
            }

            .metadata {
                border-bottom: medium solid blue;
                display: inline-block;
                padding: 5px;
                width: 100%;
            }

            .annotations {
                padding: 5px;
            }

            .hidden {
                display: none;
            }

            .buttons {
                padding: 10px;
                cursor: pointer;
            }
        </style>
    </head>

    <body>
        {% for func_key in func_data.keys() %}
            <div class="metadata">
            Function name: {{func_data[func_key]['funcname']}}<br />
            {% if func_data[func_key]['filename'] %}
                in file: {{func_data[func_key]['filename']|escape}}<br />
            {% endif %}
            with signature: {{func_key[1]|e}}
            </div>
            <div class="annotations">
            <table class="annotation_table tex2jax_ignore">
                {%- for num, line, hl, hc in func_data[func_key]['pygments_lines'] -%}
                    {%- if func_data[func_key]['ir_lines'][num] %}
                        <tr><td style="text-align:left;" class="{{func_data[func_key]['python_tags'][num]}}">
                            <code>
                            {{func_data[func_key]['N'] % num}}:
                            {{'&nbsp;'*func_data[func_key]['python_indent'][num]}}{{hl}}
                            </code>
                        </td></tr>
                    {% else -%}
                        <tr><td style="text-align:left;" class="{{func_data[func_key]['python_tags'][num]}}">
                            <code>
                                {{func_data[func_key]['N'] % num}}:
                                {{'&nbsp;'*func_data[func_key]['python_indent'][num]}}{{hl}}
                            </code>
                        </td></tr>
                    {%- endif -%}
                {%- endfor -%}
            </table>
            </div>
        {% endfor %}
    </body>
    </html>
    """)

def get_html_template_bytecode():
    try:
        from jinja2 import Template
    except ImportError:
        raise ImportError("please install the 'jinja2' package")
    return Template("""
    <html>
    <head>
        <style>

            .annotation_table {
                color: #000000;
                font-family: italic;
                margin: 5px;
                width: 100%;
            }

            /* override JupyterLab style */
            .annotation_table td {
                text-align: left;
                background-color: white; /*Might change: transparent*/
                padding: 1px;
            }

            .annotation_table tbody tr:nth-child(even) {
                background: white;
            }

            .annotation_table code
            {
                background-color: white; /*Might change: transparent*/
                white-space: normal;
                font-size: large;
                font-style: italics;
            }

            /* End override JupyterLab style */

            tr:hover {
                background-color: rgba(92, 200, 249, 0.25);
            }

            td.object_tag summary ,
            td.lifted_tag summary{
                font-weight: bold;
                display: list-item;
            }

            span.lifted_tag {
                color: #00cc33;
            }

            span.object_tag {
                color: #cc3300;
            }


            td.lifted_tag {
                background-color: #cdf7d8;
            }

            td.object_tag {
                background-color: #fef5c8;
            }

            code.ir_code {
                color: white;
                font-style: italic;
            }

            .metadata {
                border-bottom: medium solid blue;
                display: inline-block;
                padding: 5px;
                width: 100%;
            }

            .annotations {
                padding: 5px;
            }

            .hidden {
                display: none;
            }

            .buttons {
                padding: 10px;
                cursor: pointer;
            }
        </style>
    </head>

    <body>
        {% for func_key in func_data.keys() %}
            <div class="metadata">
            Function name: {{func_data[func_key]['funcname']}}<br />
            {% if func_data[func_key]['filename'] %}
                in file: {{func_data[func_key]['filename']|escape}}<br />
            {% endif %}
            with signature: {{func_key[1]|e}}
            </div>
            <div class="annotations">
            <table class="annotation_table tex2jax_ignore">
                {%- for num, line, hl, hc in func_data[func_key]['pygments_lines'] -%}
                    {%- if func_data[func_key]['bytecode_lines'][num] %}
                        <tr><td style="text-align:left;" class="{{func_data[func_key]['python_tags'][num]}}">
                            <details>
                                <summary>
                                    <code>
                                    {{func_data[func_key]['N'] % num}}:
                                    {{'&nbsp;'*func_data[func_key]['python_indent'][num]}}{{hl}}
                                    </code>
                                </summary>
                                <table class="annotation_table">
                                    <tbody>
                                        {%- for ir_num, ir_line in func_data[func_key]['bytecode_lines_'+num|string] %}
                                            <tr class="ir_code">
                                                <td style="text-align: left;">
                                                    <code>
                                                        {{'&nbsp;'*func_data[func_key]['bytecode_indent'][num][ir_num-1]}}{{ir_line}}
                                                    </code>
                                                </td>
                                            </tr>
                                        {%- endfor -%}
                                    </tbody>
                                </table>
                            </details>
                        </td></tr>
                    {% else -%}
                        <tr><td style="text-align:left;" class="{{func_data[func_key]['python_tags'][num]}}">
                            <code>
                                {{func_data[func_key]['N'] % num}}:
                                {{'&nbsp;'*func_data[func_key]['python_indent'][num]}}{{hl}}
                            </code>
                        </td></tr>
                    {%- endif -%}
                {%- endfor -%}
            </table>
            </div>
        {% endfor %}
    </body>
    </html>
    """)

def get_html_template_ptx():
    try:
        from jinja2 import Template
    except ImportError:
        raise ImportError("please install the 'jinja2' package")
    return Template("""
    <html>
    <head>
        <style>

            .annotation_table {
                color: #000000;
                font-family: italic;
                margin: 5px;
                width: 100%;
            }

            /* override JupyterLab style */
            .annotation_table td {
                text-align: left;
                background-color: white; /*Might change: transparent*/
                padding: 1px;
            }

            .annotation_table tbody tr:nth-child(even) {
                background: white;
            }

            .annotation_table code
            {
                background-color: white; /*Might change: transparent*/
                white-space: normal;
                font-size: large;
                font-style: italics;
            }

            /* End override JupyterLab style */

            tr:hover {
                background-color: rgba(92, 200, 249, 0.25);
            }

            td.object_tag summary ,
            td.lifted_tag summary{
                font-weight: bold;
                display: list-item;
            }

            span.lifted_tag {
                color: #00cc33;
            }

            span.object_tag {
                color: #cc3300;
            }


            td.lifted_tag {
                background-color: #cdf7d8;
            }

            td.object_tag {
                background-color: #fef5c8;
            }

            code.ir_code {
                color: white;
                font-style: italic;
            }

            .metadata {
                border-bottom: medium solid blue;
                display: inline-block;
                padding: 5px;
                width: 100%;
            }

            .annotations {
                padding: 5px;
            }

            .hidden {
                display: none;
            }

            .buttons {
                padding: 10px;
                cursor: pointer;
            }
        </style>
    </head>

    <body>
        {% for func_key in func_data.keys() %}
            <div class="metadata">
            Function name: {{func_data[func_key]['funcname']}}<br />
            {% if func_data[func_key]['filename'] %}
                in file: {{func_data[func_key]['filename']|escape}}<br />
            {% endif %}
            with signature: {{func_key[1]|e}}
            </div>
            <div class="annotations">
            <table class="annotation_table tex2jax_ignore">
                {%- for num, line, hl, hc in func_data[func_key]['pygments_lines'] -%}
                    {%- if func_data[func_key]['ptx_lines'][num] %}
                        <tr><td style="text-align:left;" class="{{func_data[func_key]['python_tags'][num]}}">
                            <details>
                                <summary>
                                    <code>
                                    {{func_data[func_key]['N'] % num}}:
                                    {{'&nbsp;'*func_data[func_key]['python_indent'][num]}}{{hl}}
                                    </code>
                                </summary>
                                <table class="annotation_table">
                                    <tbody>
                                        {%- for ir_num, ir_lines, ir_hl, ir_hc in func_data[func_key]['pygments_ptx_lines_'+num|string] %}
                                            <tr class="ir_code">
                                                <td style="text-align: left;">
                                                    <code>
                                                        {{'&nbsp;'*func_data[func_key]['ptx_indent'][num][ir_num-1]}}{{ir_hl}}
                                                    </code>
                                                </td>
                                            </tr>
                                        {%- endfor -%}
                                    </tbody>
                                </table>
                            </details>
                        </td></tr>
                    {% else -%}
                        <tr><td style="text-align:left;" class="{{func_data[func_key]['python_tags'][num]}}">
                            <code>
                                {{func_data[func_key]['N'] % num}}:
                                {{'&nbsp;'*func_data[func_key]['python_indent'][num]}}{{hl}}
                            </code>
                        </td></tr>
                    {%- endif -%}
                {%- endfor -%}
            </table>
            </div>
        {% endfor %}
    </body>
    </html>
    """)

def get_html_template_ptx_gray():
    try:
        from jinja2 import Template
    except ImportError:
        raise ImportError("please install the 'jinja2' package")
    return Template("""
    <html>
    <head>
        <style>

            .annotation_table {
                color: #000000;
                font-family: italic;
                margin: 5px;
                width: 100%;
            }

            /* override JupyterLab style */
            .annotation_table td {
                text-align: left;
                background-color: white; /*Might change: transparent*/
                padding: 1px;
            }

            .annotation_table tbody tr:nth-child(even) {
                background: white;
            }

            .annotation_table code
            {
                background-color: white; /*Might change: transparent*/
                white-space: normal;
                font-size: large;
                font-style: italics;
            }

            /* End override JupyterLab style */

            tr:hover {
                background-color: rgba(92, 200, 249, 0.25);
            }

            td.object_tag summary ,
            td.lifted_tag summary{
                font-weight: bold;
                display: list-item;
            }

            span.lifted_tag {
                color: #00cc33;
            }

            span.object_tag {
                color: #cc3300;
            }


            td.lifted_tag {
                background-color: #cdf7d8;
            }

            td.object_tag {
                background-color: #fef5c8;
            }

            code.ir_code {
                color: white;
                font-style: italic;
            }

            .metadata {
                border-bottom: medium solid blue;
                display: inline-block;
                padding: 5px;
                width: 100%;
            }

            .annotations {
                padding: 5px;
            }

            .hidden {
                display: none;
            }

            .buttons {
                padding: 10px;
                cursor: pointer;
            }
        </style>
    </head>

    <body>
        {% for func_key in func_data.keys() %}
            <div class="metadata">
            Function name: {{func_data[func_key]['funcname']}}<br />
            {% if func_data[func_key]['filename'] %}
                in file: {{func_data[func_key]['filename']|escape}}<br />
            {% endif %}
            with signature: {{func_key[1]|e}}
            </div>
            <div class="annotations">
            <table class="annotation_table tex2jax_ignore">
                {%- for num, line, hl, hc in func_data[func_key]['pygments_lines'] -%}
                    {%- if func_data[func_key]['ptx_lines'][num] %}
                        <tr><td style="text-align:left;" class="{{func_data[func_key]['python_tags'][num]}}">
                            <details>
                                <summary>
                                    <code>
                                    {{func_data[func_key]['N'] % num}}:
                                    {{'&nbsp;'*func_data[func_key]['python_indent'][num]}}{{hl}}
                                    </code>
                                </summary>
                                <table class="annotation_table">
                                    <tbody>
                                        {%- for ir_line in func_data[func_key]['ptx_lines'][num] %}
                                            <tr class="ir_code">
                                                <td style="text-align: left;">
                                                    <code>
                                                        {{'&nbsp;'*func_data[func_key]['ptx_indent'][num][loop.index0]}}{{ir_line}}
                                                    </code>
                                                </td>
                                            </tr>
                                        {%- endfor -%}
                                    </tbody>
                                </table>
                            </details>
                        </td></tr>
                    {% else -%}
                        <tr><td style="text-align:left;" class="{{func_data[func_key]['python_tags'][num]}}">
                            <code>
                                {{func_data[func_key]['N'] % num}}:
                                {{'&nbsp;'*func_data[func_key]['python_indent'][num]}}{{hl}}
                            </code>
                        </td></tr>
                    {%- endif -%}
                {%- endfor -%}
            </table>
            </div>
        {% endfor %}
    </body>
    </html>
    """)

def reform_code(annotation):
    """
    Extract the code from the Numba annotation datastructure. 

    Pygments can only highlight full multi-line strings, the Numba
    annotation is list of single lines, with indentation removed.
    """
    ident_dict = annotation['python_indent']
    s= ''
    for n,l in annotation['python_lines']:
        s = s+' '*ident_dict[n]+l+'\n'
    return s

def reform_ir_code(annotation, i):
    """
    Extract the code from the Numba annotation datastructure. 

    Pygments can only highlight full multi-line strings, the Numba
    annotation is list of single lines, with indentation removed.
    """
    ident_dict = annotation['ir_indent']
    s= ''
    for n,l in annotation[f'ir_lines_{i}']:
        s = s+' '*ident_dict[i][n-1]+l+'\n'
    return s

def reform_bytecode_code(annotation, i):
    ident_dict = annotation['bytecode_indent']
    s= ''
    for n,l in annotation[f'bytecode_lines_{i}']:
        try:
            s = s+' '*ident_dict[i][n-1]+l+'\n'
        except TypeError:
            s = s+' '*ident_dict[i][n-1]+l[0]+'\n'
    return s

def reform_ptx_code(annotation, i):
    ident_dict = annotation['ptx_indent']
    s= ''
    for n,l in annotation[f'ptx_lines_{i}']:
        try:
            s = s+' '*ident_dict[i][n-1]+l+'\n'
        except TypeError:
            s = s+' '*ident_dict[i][n-1]+l[0]+'\n'
    return s

def seperate_ir_lines(annotation):
    ir = list(annotation.items())[0][1]['ir_lines']
    lines = [l for l in ir.keys() if ir[l] != []]
    for i in lines:
        list(annotation.items())[0][1][f'ir_lines_{i}'] = [(j+1, l[0]) for j, l in enumerate(ir[i])]


def seperate_bytecode_lines(annotation):
    ir = list(annotation.items())[0][1]['bytecode_lines']
    lines = [l for l in ir.keys() if ir[l] != []]
    for i in lines:
        list(annotation.items())[0][1][f'bytecode_lines_{i}'] = [(j+1, l) for j, l in enumerate(ir[i])]

def seperate_ptx_lines(annotation):
    ir = list(annotation.items())[0][1]['ptx_lines']
    lines = [l for l in ir.keys() if ir[l] != []]
    for i in lines:
        list(annotation.items())[0][1][f'ptx_lines_{i}'] = [(j+1, l) for j, l in enumerate(ir[i])]

class Annotate:
    def __init__(self, function, signature=None, **kwargs):
        self.function = function
        style = kwargs.get('style', 'default')
        if not function.signatures:
            raise ValueError('function need to be jitted for at least one signature')
        ann = function.get_annotation_info(signature=signature)
        self.ann = ann
        self.python_lines = kwargs.get('python_lines', None)
        self.python_indent = kwargs.get('python_indent', None)
        if self.python_lines:
            list(ann.items())[0][1]['python_lines'] = self.python_lines
        if self.python_indent:
            list(ann.items())[0][1]['python_indent'] = self.python_indent

        for k,v in ann.items():
            res = hllines(reform_code(v), style)
            rest = htlines(reform_code(v), style)
            v['pygments_lines'] = [(a,b,c, d) for (a,b),c, d in zip(v['python_lines'], res, rest)]

        import math
        list(ann.items())[0][1]['N'] = f"%0{int(math.log10(len(list(ann.items())[0][1]['python_lines']))+1)}d"
        seperate_ir_lines(ann)
        ir = list(ann.items())[0][1]['ir_lines']
        lines = [l for l in ir.keys() if ir[l] != []]
        for i in lines:
            for k,v in ann.items():
                res = hllines_ir(reform_ir_code(v, i), style)
                rest = htlines_ir(reform_ir_code(v, i), style)
                v[f'pygments_ir_lines_{i}'] = [(a,b,c,d) for (a,b),c,d in zip(v[f'ir_lines_{i}'], res, rest)] # Batch into pygments_ir_lines_1, 2, ...

    def _repr_html_(self):
        return get_html_template().render(func_data=self.ann)

class Annotate2:
    def __init__(self, function, signature=None, **kwargs):
        self.function = function
        style = kwargs.get('style', 'default')
        if not function.signatures:
            raise ValueError('function need to be jitted for at least one signature')
        ann = function.get_annotation_info(signature=signature)
        self.ann = ann
        self.python_lines = kwargs.get('python_lines', None)
        self.python_indent = kwargs.get('python_indent', None)
        if self.python_lines:
            list(ann.items())[0][1]['python_lines'] = self.python_lines
        if self.python_indent:
            list(ann.items())[0][1]['python_indent'] = self.python_indent

        for k,v in ann.items():
            res = hllines(reform_code(v), style)
            rest = htlines(reform_code(v), style)
            v['pygments_lines'] = [(a,b,c, d) for (a,b),c, d in zip(v['python_lines'], res, rest)]

        import math
        list(ann.items())[0][1]['N'] = f"%0{int(math.log10(len(list(ann.items())[0][1]['python_lines']))+1)}d"
        seperate_ir_lines(ann)
        ir = list(ann.items())[0][1]['ir_lines']
        lines = [l for l in ir.keys() if ir[l] != []]
        for i in lines:
            for k,v in ann.items():
                res = hllines_ir(reform_ir_code(v, i), style)
                rest = htlines_ir(reform_ir_code(v, i), style)
                v[f'pygments_ir_lines_{i}'] = [(a,b,c,d) for (a,b),c,d in zip(v[f'ir_lines_{i}'], res, rest)] # Batch into pygments_ir_lines_1, 2, ...

    def _repr_html_(self):
        return get_html_template2().render(func_data=self.ann)

class AnnotateBytecode:
    def __init__(self, function, signature=None, **kwargs):
        self.function = function
        style = kwargs.get('style', 'default')
        if not function.signatures:
            raise ValueError('function need to be jitted for at least one signature')
        ann = function.get_annotation_info(signature=signature)
        self.ann = ann
        self.python_lines = kwargs.get('python_lines', None)
        self.python_indent = kwargs.get('python_indent', None)
        self.bytecode_lines = kwargs.get('bytecode_lines', None)
        self.bytecode_indent = kwargs.get('bytecode_indent', None)
        
        if self.python_lines:
            list(ann.items())[0][1]['python_lines'] = self.python_lines
        if self.python_indent:
            list(ann.items())[0][1]['python_indent'] = self.python_indent
        if self.bytecode_lines:
            list(ann.items())[0][1]['bytecode_lines'] = self.bytecode_lines
        if self.bytecode_indent:
            list(ann.items())[0][1]['bytecode_indent'] = self.bytecode_indent

        for k,v in ann.items():
            res = hllines(reform_code(v), style)
            rest = htlines(reform_code(v), style)
            v['pygments_lines'] = [(a,b,c, d) for (a,b),c, d in zip(v['python_lines'], res, rest)]

        import math
        list(ann.items())[0][1]['N'] = f"%0{int(math.log10(len(list(ann.items())[0][1]['python_lines']))+1)}d"
        seperate_bytecode_lines(ann)

    def _repr_html_(self):
        return get_html_template_bytecode().render(func_data=self.ann)

class AnnotatePTX:
    def __init__(self, function, signature=None, **kwargs):
        self.function = function
        style = kwargs.get('style', 'default')
        if not function.signatures:
            raise ValueError('function need to be jitted for at least one signature')
        ann = function.get_annotation_info(signature=signature)
        self.ann = ann
        self.python_lines = kwargs.get('python_lines', None)
        self.python_indent = kwargs.get('python_indent', None)
        self.ptx_lines = kwargs.get('ptx_lines', None)
        self.ptx_indent = kwargs.get('ptx_indent', None)
        
        if self.python_lines:
            list(ann.items())[0][1]['python_lines'] = self.python_lines
        if self.python_indent:
            list(ann.items())[0][1]['python_indent'] = self.python_indent
        if self.ptx_lines:
            list(ann.items())[0][1]['ptx_lines'] = self.ptx_lines
        if self.ptx_indent:
            list(ann.items())[0][1]['ptx_indent'] = self.ptx_indent

        for k,v in ann.items():
            res = hllines(reform_code(v), style)
            rest = htlines(reform_code(v), style)
            v['pygments_lines'] = [(a,b,c, d) for (a,b),c, d in zip(v['python_lines'], res, rest)]

        import math
        list(ann.items())[0][1]['N'] = f"%0{int(math.log10(len(list(ann.items())[0][1]['python_lines']))+1)}d"
        seperate_ptx_lines(ann)
        ir = list(ann.items())[0][1]['ptx_lines']
        lines = [l for l in ir.keys() if ir[l] != []]
        for i in lines:
            for k,v in ann.items():
                res = hllines_ptx(reform_ptx_code(v, i), style)
                rest = htlines_ptx(reform_ptx_code(v, i), style)
                v[f'pygments_ptx_lines_{i}'] = [(a,b,c,d) for (a,b),c,d in zip(v[f'ptx_lines_{i}'], res, rest)] # Batch into pygments_ir_lines_1, 2, ...

    def _repr_html_(self):
        return get_html_template_ptx().render(func_data=self.ann)

class AnnotatePTXGray:
    def __init__(self, function, signature=None, **kwargs):
        self.function = function
        style = kwargs.get('style', 'default')
        if not function.signatures:
            raise ValueError('function need to be jitted for at least one signature')
        ann = function.get_annotation_info(signature=signature)
        self.ann = ann
        self.python_lines = kwargs.get('python_lines', None)
        self.python_indent = kwargs.get('python_indent', None)
        self.ptx_lines = kwargs.get('ptx_lines', None)
        self.ptx_indent = kwargs.get('ptx_indent', None)
        
        if self.python_lines:
            list(ann.items())[0][1]['python_lines'] = self.python_lines
        if self.python_indent:
            list(ann.items())[0][1]['python_indent'] = self.python_indent
        if self.ptx_lines:
            list(ann.items())[0][1]['ptx_lines'] = self.ptx_lines
        if self.ptx_indent:
            list(ann.items())[0][1]['ptx_indent'] = self.ptx_indent

        for k,v in ann.items():
            res = hllines(reform_code(v), style)
            rest = htlines(reform_code(v), style)
            v['pygments_lines'] = [(a,b,c, d) for (a,b),c, d in zip(v['python_lines'], res, rest)]

        import math
        list(ann.items())[0][1]['N'] = f"%0{int(math.log10(len(list(ann.items())[0][1]['python_lines']))+1)}d"

    def _repr_html_(self):
        return get_html_template_ptx_gray().render(func_data=self.ann)