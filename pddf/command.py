import pandas as pd
from otlang.sdk.syntax import Keyword, Positional, Subsearch, OTLType
from pp_exec_env.base_command import BaseCommand, Syntax


class PddfCommand(BaseCommand):
    syntax = Syntax(
        [
            Positional("function", required=True, otl_type=OTLType.TEXT),
            Positional("columns", inf=True, otl_type=OTLType.ALL),
            Keyword("kwargs", inf=True, otl_type=OTLType.ALL),
            Keyword("subsearch_to_positional_list", required=False, otl_type=OTLType.ALL),
            Keyword("subsearch_key", required=False, otl_type=OTLType.TEXT),
            Keyword("column_to_string", required=False, otl_type=OTLType.ALL),
            Keyword("force_reset_index", required=False, otl_type=OTLType.ALL),
            Subsearch("subsearches", required=False, inf=True)
        ]
    )

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        self.log_progress('Start pddf command')
        self.log_progress('Loading columns', stage=1, total_stages=4)
        cols = [col.value for col in self.get_iter("columns")]
        col_to_str = self.get_arg("column_to_string").value
        if col_to_str:
            self.logger.info("col_to_str was passed: using as a Series indexer")
            cols = cols[0]
        if not cols:
            cols = df.columns
        df = df[cols]

        self.log_progress("Loading function", stage=2, total_stages=4)
        fname = self.get_arg("function").value
        if fname == 'eval':
            raise ValueError('Eval function not allowed')
        func = df.__getattr__(fname)

        self.log_progress("Loading function arguments", stage=3, total_stages=4)
        kwargs = {}
        for kwarg in self.get_iter("kwargs"):
            kwargs[kwarg.key] = kwarg.value

        subsearches = [sub.value for sub in self.get_iter("subsearches")]
        if to_list := self.get_arg("subsearch_to_positional_list").value:
            subsearches = [subsearches]

        if key := self.get_arg("subsearch_key").value:
            if to_list:
                raise ValueError("Cannot make subsearches positional with key")
            kwargs[key] = subsearches.copy()
            subsearches = []

        self.log_progress(f"Executing function {fname}", stage=4, total_stages=4)
        df = func(*subsearches, **kwargs)

        if isinstance(df, pd.Series) or self.get_arg("force_reset_index").value:
            self.logger.info("Resetting index")
            df = df.reset_index()

        return df
