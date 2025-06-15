use std::fs;
use clap::Parser;
use anyhow::Result;

#[derive(Parser)]
#[command(author, version, about, long_about = None)]
struct Args {
    /// The source file to run
    file: String,
}

fn main() -> Result<()> {
    let args = Args::parse();
    let source = fs::read_to_string(&args.file)?;
    
    // Parse and interpret the source code
    let program = belasova::parser::parse(&source)?;
    let interpreter = belasova::interpreter::Interpreter::new();
    interpreter.interpret(program);
    
    Ok(())
} 