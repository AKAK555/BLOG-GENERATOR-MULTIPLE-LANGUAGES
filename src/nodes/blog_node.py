from src.states.blogstate import BlogState
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from src.states.blogstate import Blog


class BlogNode:
    """
    A class to represent the blog node
    """

    def __init__(self, llm):
        self.llm = llm

    def _to_text(self, obj):
        """
        Normalize various LLM return shapes into a plain string:
        - AIMessage / message-like objects -> .content
        - dict -> try common keys
        - dataclass / object -> try .content or str()
        - string -> return as-is
        """
        if obj is None:
            return ""
        # message-like
        try:
            if hasattr(obj, "content"):
                return getattr(obj, "content") or str(obj)
        except Exception:
            pass

        # dict-like
        if isinstance(obj, dict):
            for k in ("content", "text", "message", "summary"):
                if k in obj and obj[k]:
                    return str(obj[k])
            # fallback stringify dict
            return str(obj)

        # plain string
        if isinstance(obj, str):
            return obj

        # object with attributes (structured output)
        try:
            # Blog structured output might be dataclass-like with .content or .title
            if hasattr(obj, "content"):
                return getattr(obj, "content") or str(obj)
            if hasattr(obj, "title") and hasattr(obj, "content"):
                # join title + content if both present
                t = getattr(obj, "title", "") or ""
                c = getattr(obj, "content", "") or ""
                return (t + "\n\n" + c).strip() if (t or c) else str(obj)
        except Exception:
            pass

        # final fallback
        try:
            return str(obj)
        except Exception:
            return ""

    def title_creation(self, state: BlogState):
        """
        create the title for the blog
        """
        if "topic" in state and state["topic"]:
            prompt = (
                "You are an expert blog content writer. Use Markdown formatting. "
                "Generate a blog title for the {topic}. This title should be creative and SEO-friendly."
            )
            system_message = prompt.format(topic=state["topic"])
            # invoke LLM - normalize return
            response = self.llm.invoke(system_message)
            title_text = self._to_text(response)
            return {"blog": {"title": title_text}}
        return {}

    def content_generation(self, state: BlogState):
        if "topic" in state and state["topic"]:
            system_prompt = (
                "You are an expert blog writer. Use markdown formatting. "
                "Generate a blog content with detailed breakdown for the {topic}"
            )
            system_message = system_prompt.format(topic=state["topic"])
            response = self.llm.invoke(system_message)
            content_text = self._to_text(response)

            # If title already present in state, preserve it; otherwise empty string
            title = ""
            try:
                title = state.get("blog", {}).get("title", "") or ""
            except Exception:
                title = ""

            return {"blog": {"title": title, "content": content_text}}
        return {}

    def translation(self, state: BlogState):
        """
        Translate the content to the specified language.
        Returns a dict state update (never a raw string).
        """
        # Defensive guard
        blog_content = ""
        try:
            blog_content = state.get("blog", {}).get("content", "") or ""
        except Exception:
            blog_content = ""

        if not blog_content:
            return {"blog": {"title": state.get("blog", {}).get("title", ""), "content": ""}}

        translation_prompt = (
            "Translate the following content into {current_language}.\n"
            "- Maintain the original tone, style and formatting.\n"
            "- Adapt cultural references and idioms to be appropriate for {current_language}.\n\n"
            "ORIGINAL CONTENT: {blog_content}\n"
        )

        messages = [
            HumanMessage(
                translation_prompt.format(
                    current_language=state.get("current_language", "english"),
                    blog_content=blog_content,
                )
            )
        ]

        # Use structured output if you're expecting Blog shape, but normalize whatever returns
        try:
            raw_translation = self.llm.with_structured_output(Blog).invoke(messages)
        except Exception:
            # fallback to a plain invoke if structured fails
            raw_translation = self.llm.invoke(messages)

        translated_text = self._to_text(raw_translation)

        # preserve title if exists
        title = state.get("blog", {}).get("title", "") or ""

        # Return a dict (LangGraph expects dict updates)
        return {"blog": {"title": title, "content": translated_text}}

    def route(self, state: BlogState):
        # simply copy current_language into state to make it explicit
        return {"current_language": state.get("current_language")}

    def route_decision(self, state: BlogState):
        """Route the content to respective translation function"""
        lang = (state.get("current_language") or "").strip().lower()
        if lang == "hindi":
            return "hindi"
        elif lang == "french":
            return "french"
        else:
            return lang or ""
