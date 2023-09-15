from collections import Counter
import random
from sec_parser.parsing_engine.html_parser import HtmlParser
from sec_parser.parsing_plugins import text_plugin
from sec_parser.parsing_plugins.highlighted_section_plugin import HighlightedPlugin
from sec_parser.parsing_plugins.root_section_plugin import RootSectionPlugin
from sec_parser.semantic_elements.semantic_elements import HighlightedElement, RootSectionElement, UnclaimedElement
import streamlit as st
from _ui import (
    st_hide_streamlit_element,
    SecApiIoApiKeyGetter,
    st_radio,
    st_multiselect_allow_long_titles,
    st_expander_allow_nested,
)

st_expander_allow_nested()
from _sec_parser import (
    download_html_from_ticker,
    download_html_from_url,
    get_semantic_elements,
    get_semantic_tree,
)
from _utils import remove_ix_tags, add_spaces
from dotenv import load_dotenv
import streamlit_antd_components as sac
import sec_parser as sp

load_dotenv()


st.set_page_config(
    page_icon="🏦",
    page_title="SEC Parser Output Visualizer",
    layout="centered",
    initial_sidebar_state="expanded",
)
st_hide_streamlit_element("class", "stDeployButton")
st_multiselect_allow_long_titles()

with st.sidebar:
    st.write("# Select Report")
    sec_api_io_key_getter = SecApiIoApiKeyGetter(st.container())

    data_source_options = [
        "Select Ticker to Find Latest",
        "Enter Ticker to Find Latest",
        "Enter SEC EDGAR URL",
    ]
    select_ticker, find_ticker, url = st_radio(
        "Select 10-Q Report Data Source", data_source_options
    )
    ticker, url = None, None
    if select_ticker:
        ticker = st.selectbox(
            label="Select Ticker",
            options=["AAPL", "GOOG"],
        )
    elif find_ticker:
        ticker = st.text_input(
            label="Enter Ticker",
            value="AAPL",
        )
    else:
        url = st.text_input(
            label="Enter URL",
            value="https://www.sec.gov/Archives/edgar/data/320193/000032019323000077/aapl-20230701.htm",
        )

    section_1_2, all_sections = st_radio(
        "Select 10-Q Sections", ["Only MD&A", "All Sections"], horizontal=True
    )
    if section_1_2:
        sections = ["part1item2"]
    else:
        sections = None


if ticker:
    html = download_html_from_ticker(
        sec_api_io_key_getter, doc="10-Q", ticker=ticker, sections=sections
    )
else:
    html = download_html_from_url(
        sec_api_io_key_getter, doc="10-Q", url=url, sections=sections
    )

view_step_options = [
    "Original From SEC EDGAR",
    "Parsed Semantic Elements",
    "Nested Semantic Tree",
]
selected_step = 1 + sac.steps(
    [
        sac.StepsItem(
            title=k.partition(" ")[0],
            description=k.partition(" ")[2],
        )
        for k in view_step_options
    ],
    index=2,
    format_func=None,
    placement="horizontal",
    size="default",
    direction="horizontal",
    type="default",  # default, navigation
    dot=False,
    return_index=True,
)


def get_pretty_class_name(element_cls, element=None):
    def get_emoji(cls):
        return {
            sp.UnclaimedElement: "🍃",
        }.get(cls, "✨")

    emoji = get_emoji(element_cls)
    level = ""
    if element and hasattr(element, "level") and element.level > 1:
        level = f" (Level {element.level})"
    class_name = f"**{add_spaces(element_cls.__name__)}{level}**"
    pretty_name = f"{emoji} {class_name}"
    return pretty_name


if selected_step > 1:
    elements = get_semantic_elements(html)
    with st.sidebar:
        st.write("# Adjust View")
        left, right = st.columns(2)
        with left:
            do_element_render_html = st.checkbox("Render HTML", value=True)
        with right:
            do_expand_all = False
            if selected_step == 2:
                do_expand_all = st.checkbox("Expand All", value=False)

        counted_element_types = Counter(element.__class__ for element in elements)
        selected_types = st.multiselect(
            "Filter Element Types",
            counted_element_types.keys(),
            counted_element_types.keys(),
            format_func=lambda cls: f'{counted_element_types[cls]}x {get_pretty_class_name(cls).replace("*","")}',
        )
        elements = [e for e in elements if e.__class__ in selected_types]

if selected_step > 2:
    tree = get_semantic_tree(elements)
    with right:
        expand_depth = st.number_input("Expand Depth", min_value=0, value=0)

if selected_step == 1:
    st.markdown(remove_ix_tags(html), unsafe_allow_html=True)


def render_semantic_element(
    element: sp.AbstractSemanticElement,
):
    bs4_tag = element.html_tag.bs4
    if do_element_render_html:
        element_html = remove_ix_tags(str(bs4_tag))
        st.markdown(element_html, unsafe_allow_html=True)
    else:
        st.code(bs4_tag.prettify(), language="html")


def render_tree_node(tree_node: sp.TreeNode, _current_depth=0):
    element = tree_node.semantic_element
    expander_title = get_pretty_class_name(element.__class__, element)
    with st.expander(expander_title, expanded=expand_depth > _current_depth):
        render_semantic_element(element)
        for child in tree_node.children:
            render_tree_node(child, _current_depth=_current_depth + 1)


if selected_step == 2:
    for element in elements:
        expander_title = get_pretty_class_name(element.__class__, element)
        with st.expander(expander_title, expanded=do_expand_all):
            render_semantic_element(element)

# my version of step 2
if selected_step == 3:
  # classe q faz ficar com o emoji
  def my_get_pretty_class_name(element_cls, element=None):
    def get_emoji(cls):
      return {
          sp.HighlightedElement: "📢",
          }.get(cls, "?")

    emoji = get_emoji(element_cls)
    level = ""
    if element and hasattr(element, "level") and element.level > 1:
      level = f" (Level {element.level})"
    class_name = f"**{add_spaces(element_cls.__name__)}{level}**"
    pretty_name = f"{emoji} {class_name}"
    return pretty_name



  for element in [HighlightedElement, RootSectionElement, UnclaimedElement]: # parse cada tag para o elemento OBS: o unclaimed fica por ultimo?
    expander_title = my_get_pretty_class_name(HighlightedElement) # oq faz alterar o titulo eh o primeiro # adicionar nome pra classe?
    with st.expander(expander_title, expanded=do_expand_all):
      raw_html =  """<b>bold text with bold tag</b>
            <p>normal text</p>
            <i>italic text with italic tag</i>
            <p>normal text</p>
            <p font-weight='700'>bold text with font-weight</p>
            """
      parser = HtmlParser()
      my_plugin = HighlightedPlugin()
      bs4_class = parser.get_root_tags(raw_html)

      semantic_elements_list = []
      for i in range(len(bs4_class)):
        semantic_elements_list.append(element(bs4_class[i]))

      applied_elements = set(my_plugin.apply(semantic_elements_list)) # reclama mas funciona

      final_return = set()
      # o problema eh q so ta usando meu plugin, retorna os outros pq nao tem validacao
      # todo: REORGANIZAR a classe e botar o for in element so no final
      # pq nao renderiza um unclaimed?
      for applied_element in applied_elements:
        print(applied_element.__class__.__name__)
        if applied_element.__class__.__name__ not in final_return:
          final_return.add(applied_element)

      # ideia 1, fazer um dicionario com o nome e a instancia da classe
      final_return_dic = {}
      for applied_element in applied_elements:
        if not final_return_dic.get(applied_element.__class__.__name__):
          final_return_dic[applied_element.__class__.__name__] = applied_element

      for element in final_return_dic.values():
        render_semantic_element(element) 




# notes:
# o tree builder receber lista de semantic ELements (nao fiz o do highlight ainda)
# o retorno da build eh uma arvore semantica q so tem self.root_nodes do tipo list[TreeNode]
# TreeNode tem propriedades: parents, children, setter, metodos: add_child, add_children, remove_child
# a tree recebe o retorno do tree builder

# para cada TreeNode, renderiza TreeNode (funcao definida no proprio app.py)

# todo:
# instanciar o builder como uma lista do meu highlighted plugin
# tentar fazer isso aparecer na ui



# obs:
# ta tudo unclaimed pq tinha uma funcao q tranformava tudo como unclaimed
# achar esse funcao
