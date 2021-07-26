mod utils;
// use std::fs::File;
use pyo3::prelude::*; // Python importing
use pyo3::ffi;
use widestring::WideCString;
use clap::{Arg, App};

fn main() -> PyResult<()> {
    
    /* Use a clap package to handle command line parsing and put into a struct */
    let matches = App::new("TMap Program")
    .author("Kyla Levin, kateri.lalicker@tufts.edu")
    .version("1.0")
    .about("TMap Program")
    .arg(
        Arg::new("disease")
        .short('p')
        .long("parkinsons")
    )
    .arg(
        Arg::new("algorithm")
        .required(true)
        .takes_value(true)
    )
    .arg(
        Arg::new("alpha")
        .required(true)
        .takes_value(true)
    )
    .arg(
        Arg::new("k_value")
        .required(true)
        .takes_value(true)
    )
    .arg(
        Arg::new("dataset")
        .required(true)
        .takes_value(true)
    )
    .get_matches();

    let mut conda_command = "".to_owned();
    // let mut tests = "".to_owned();
    let mut imports = "".to_owned();
    let mut config = "".to_owned();
    let mut data_set = "".to_owned();
    let mut model_set = "".to_owned();
    let data = matches.value_of("dataset").unwrap();
    let algo = matches.value_of("algorithm").unwrap();
    let alpha = matches.value_of("alpha").unwrap();
    let k_value = matches.value_of("k_value").unwrap();

    let mut pd = false;
    if matches.is_present("disease") {
        // tests.push_str("print('Evaluating Parkinsons')\n");
        pd = true;
    }
    // else {
    //     tests.push_str("print('Evaluating Alzheimers')\n");
    // }

    // tests.push_str("print('Alpha value is ");
    // tests.push_str(alpha);
    // tests.push_str("')\n");
    // tests.push_str("print('K value is ");
    // tests.push_str(k_value);
    // tests.push_str("')\n");

    if data == "huri" {
        imports.push_str("from t_map.garbanzo.huri import Huri\n");
        // tests.push_str("print('Running huri dataset')\n");
        if pd {
            data_set.push_str("data = Huri('./data/parkinsons', with_hugo=True)\n");
        }
        else {
            data_set.push_str("data = Huri('./data/alzheimers', with_hugo=True)\n");
        }
    }
    else {
        imports.push_str("print('Sorry, don't recognize that dataset.')\n");
    }

    imports.push_str(r#"
from t_map.hummus.hummus import Hummus
from t_map.hummus.hummus_score import HummusScore, ScoreTypes
"#);

    if algo == "rwr" {
        imports.push_str("from t_map.feta.randomwalk import RandomWalkWithRestart, PreComputeRWR\n");
        model_set.push_str("model = RandomWalkWithRestart(alpha=config['alpha'])\n");
        // tests.push_str("print('Running RWR')\n");
    }
    else {
        imports.push_str("print('Sorry, don't recognize that algorithm.')\n");
    }

    config.push_str("config = { 'alpha': ");
    config.push_str(alpha);
    config.push_str(", 'k': ");
    config.push_str(k_value);
    config.push_str(", }\n");

    data_set.push_str(r#"scoring = HummusScore(score_type=ScoreTypes.TOP_K, k=config['k'])
runner = Hummus(data, with_scoring=scoring)
"#);
    model_set.push_str(r#"genes = {data.get(i).name for i in range(len(data))}
nodes = set(data.graph.nodes)
print(len(genes.intersection(nodes)), len(genes))
"#);

    // conda_command.push_str(&tests);
    conda_command.push_str(&imports);
    conda_command.push_str(&config);
    conda_command.push_str(&data_set);
    conda_command.push_str(&model_set);

    if let Some(PYTHONHOME) = std::env::var_os("CONDA_PREFIX") {
        unsafe {
            ffi::Py_SetPythonHome(
                WideCString::from_str(PYTHONHOME.to_str().unwrap())
                    .unwrap()
                    .as_ptr() as *const i32,
            );
        }
    }

    pyo3::prepare_freethreaded_python();

    // let gil = Python::acquire_gil();
    // let py = gil.python();
    Python::with_gil(|py|{
        let result = py.run(&conda_command, None, None);

    if let Err(ref err) = result {
        println!("{:?}", err);
    }

    });
    
    Ok(())
}