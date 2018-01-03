/**
 * run_nyc.cpp
 * 
 * Run the NYC taxi dataset cleaning task.
 */

#ifdef __linux__
#define _BSD_SOURCE 500
#define _POSIX_C_SOURCE 2
#endif

#include <algorithm>
#include <ctime>
#include <iostream>
#include <fstream>
#include <sstream>
#include <stdlib.h>
#include <stdio.h>
#include <stdint.h>
#include <assert.h>
#include <string.h>
#include <unistd.h>
#include <sys/time.h>
#include <omp.h>

#include <vector>
#include <random>
#include <boost/random/uniform_int_distribution.hpp>
static std::default_random_engine generator( time( NULL ) ^ getpid() );

using namespace std;

int uniform_int( int range ) {
  boost::random::uniform_int_distribution<> rand( 0, range );
  return rand( generator );
}

#include "weld.h"

// Value for the predicate to pass.
#define PASS 19940101.0
#define FAIL 19930101.0

vector<vector<double>> read_csv( string fname, bool header ) {
  ifstream csvf( fname );
  vector<vector<double>> items;

  bool got_header = false;
  while( csvf.good() and getline( csvf ) ) {
    if ( !got_header and header ) {
      got_header = true;
      continue;
    }
    
    stringstream ss( fname );
    string item;
    vector<double> line;

    while( getline(ss, item, ',') ) {
      line.push_back( atof(item.c_str()) ); 
    }

    items.push_back( line );
  }

  return items;
}

// The generated input data.
class gen_data {
public:
  vector<vector<double>> items_;
  uint32_t num_items_;
  uint32_t num_columns_;

  gen_data(string filename, bool header) :
    items_( read_csv(filename, header) ),
    num_items_( items_.size() ),
    num_columns_( items_[0].size() ) {
  }
};

template <typename T>
struct weld_vector {
    T *data;
    int64_t length;
};

template <typename T>
weld_vector<T> make_weld_vector(T *data, int64_t length) {
    struct weld_vector<T> vector;
    vector.data = data;
    vector.length = length;
    return vector;
}

double run_query_weld(const char* fname, struct gen_data *d, string passes) {
    // Compile Weld module.
    weld_error_t e = weld_error_new();
    weld_conf_t conf = weld_conf_new();
    //    weld_conf_set(conf, "weld.compile.dumpCode", "true");
    weld_conf_set(conf, "weld.optimization.passes", passes.c_str());
    
    FILE *fptr = fopen(fname, "r");
    fseek(fptr, 0, SEEK_END);
    int string_size = ftell(fptr);
    rewind(fptr);
    char *program = (char *) malloc(sizeof(char) * (string_size + 1));
    fread(program, sizeof(char), string_size, fptr);
    program[string_size] = '\0';
    
    struct timeval start, end, diff;
    gettimeofday(&start, 0);
    weld_module_t m = weld_module_compile(program, conf, e);
    weld_conf_free(conf);

    gettimeofday(&end, 0);
    timersub(&end, &start, &diff);
    //printf("Weld compile time: %ld.%06ld\n",
    //       (long) diff.tv_sec, (long) diff.tv_usec);

    if (weld_error_code(e)) {
        const char *err = weld_error_message(e);
        printf("Error message: %s\n", err);
        exit(1);
    }

   gettimeofday(&start, 0);

   vector<weld_vector<double>> args;
   for ( uint32_t i = 0; i < d->num_columns_; i++ ) {
     args.push_back(make_weld_vector<double>(d->items_[i].data(), d->num_items_));
   }

   weld_value_t weld_args = weld_value_new(args.data());

   // Run the module and get the result.
    conf = weld_conf_new();
    weld_value_t result = weld_module_run(m, conf, weld_args, e);
    if (weld_error_code(e)) {
        const char* err = weld_error_message(e);
        printf("Error message: %s\n", err);
        exit(1);
    }

    double* result_data = (double*) weld_value_data(result);
    double final_result = *result_data;

    // Free the values.
    weld_value_free(result);
    weld_value_free(weld_args);
    weld_conf_free(conf);

    weld_error_free(e);
    weld_module_free(m);
    gettimeofday(&end, 0);
    timersub(&end, &start, &diff);
    // printf("Weld: %ld.%06ld (result=%.4f)\n",
    printf("%ld.%06ld\t%.4f\n", 
           (long) diff.tv_sec, (long) diff.tv_usec, final_result);

    return final_result;
}

int main(int argc, char **argv) {
    // Weld code to run.
    std::string code_fname = "unpredicate-small.weld";
    // Weld code to run.
    std::string data_fname = "data/taxi_sf\=1.csv.trunc";
    // Optimization passes.
    std::string passes = "loop-fusion unroll-static-loop infer-size inline-literals unroll-structs short-circuit-booleans inline-let predicate vectorize";
    std::replace(passes.begin(), passes.end(), ' ', ',');

    int ch;
    while ((ch = getopt(argc, argv, "d:p:f:")) != -1) {
      switch (ch) {
      case 'f':
        code_fname = optarg;
        break;
      case 'd':
        data_fname = optarg;
        break;
      case 'p':
	passes = optarg;
	break;
      case '?':
      default:
        fprintf(stderr, "invalid options");
        exit(1);
      }
    }
    
    struct gen_data d(data_fname, true);
    double result;
    struct timeval start, end, diff;

    result = run_query_weld(code_fname.c_str(), &d, passes);

    return 0;
}
