import cript as C

#
# # Connect to database
# db_username = "DW_cript"
# db_password = "YXMaoE1"
# db_project = "cript_testing"
# db_database = "test"
# user = "johndoe13@cript.edu"
# db = C.CriptDB(db_username, db_password, db_project, db_database, user)


C.Prop(key="phase", value="liquid")
C.Prop(key="color", value="colorless")
C.Prop(key="mw", value=104.15, unit=C.Unit("g/mol"), method="prescribed")
C.Prop(key="density", value=0.906, unit=C.Unit("g/ml"),
       conditions=[C.Cond(key="temp", value=25, unit=C.Unit("degC"))]
       )
C.Prop(key="bp", value=145, unit=C.Unit("degC"),
       conditions=[C.Cond(key="pressure", value=1, unit=C.Unit("atm"))]
       )
C.Prop(key="mp", value=-30, unit=C.Unit("degC"),
       conditions=[C.Cond(key="pressure", value=1, unit=C.Unit("bar"))]
       )

mat_styrene = C.Material(
    identifier=C.Iden(
        preferred_name="styrene",
        names=["vinylbenzene", "phenylethylene", "ethenylbenzene"],
        chem_formula="C8H8",
        smiles="C=Cc1ccccc1",
        cas="100-42-5",
        pubchem_cid="7501",
        inchi_key="PPBRXRYQALVLMV-UHFFFAOYSA-N"
    ),
    properties=[C.Prop(key="phase", value="liquid"),
                C.Prop(key="color", value="colorless"),
                C.Prop(key="mw", value=104.15, unit=C.Unit("g/mol"), method="prescribed"),
                C.Prop(key="density", value=0.906, unit=C.Unit("g/ml"),
                       conditions=[C.Cond(key="temp", value=25, unit=C.Unit("degC"))]
                       ),
                C.Prop(key="bp", value=145, unit=C.Unit("degC"),
                       conditions=[C.Cond(key="pressure", value=1, unit=C.Unit("atm"))]
                       ),
                C.Prop(key="mp", value=-30, unit=C.Unit("degC"),
                       conditions=[C.Cond(key="pressure", value=1, unit=C.Unit("bar"))]
                       )
                ],
    keywords=["styrene"],
    storage=[
        C.Cond(key="temp", value=-20, unit=C.Unit("degC")),
        C.Cond(key="atm", value="argon")
    ]
)
