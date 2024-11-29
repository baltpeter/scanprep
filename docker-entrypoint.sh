#!/bin/bash -xe

INPUT_DIR=/input
OUTPUT_DIR=/output

while true; do
  ls -l "$INPUT_DIR"

  for INPUT_FILE in "$INPUT_DIR"/*.pdf
  do
    if [ -f "$INPUT_FILE" ]; then
      scanprep "$INPUT_FILE" "$OUTPUT_DIR"
      rm "$INPUT_FILE"
    fi
  done

  ls -l "$OUTPUT_DIR"

  sleep ${LOOP_DELAY:-120}
done
