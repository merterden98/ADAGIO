mod utils;
use std::fs::File;
use std::io::prelude::*;
use pyo3::prelude::*; // Python importing
use clap::Clap; // Command line handling

// Struct with all command line args
#[derive(Clap, Debug)]
#[clap(name = "args")]
struct Args {
    // Algorithm to run (eg. rwr)
    #[clap(short, long)]
    name: String,

    // Data set to run (.tsv file)
    #[clap(short, long)]
    name: String,

    /// Number of times to greet
    #[clap(short, long, default_value = "1")]
    count: u8,
}

fn main() -> PyResult<()> {

    /* Use a clap package to handle command line parsing and put into a struct */

    Python::with_gil(|py| {
        let GarbanzoR = PyModule::import(py, "Garbanzo")?;
        let RwrR = PyModule::import(py, "RandomWalkWithRestart")?;
        // Testing purposes
        let testFetaR = PyModule::import(py, "test_feta")?;

        testFetaR.getattr("test_rwr")?.call0()?;
        Ok(())
    })

    let mut file = File::create("output.txt")?; // Create output file with desired name
    file.write_all(b"Hello, world!")?; // Write results to output file

    // What format are the results of the algorithm be in???
    // How to send that to output file?

    Ok(())
}
