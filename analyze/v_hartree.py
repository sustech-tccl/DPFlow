#! /usr/env/bin python

import os
import csv
import math
import linecache
import numpy as np
from DPFlow.lib import statistic_mod
from DPFlow.tools import log_info
from DPFlow.tools import data_op

def calc_v_hartree(cube_file, surface, work_dir):

  '''
  calc_v_hartree: calculate v_hartree from cube file.

  Args :
    cube_file: string
      cube_file is the v_hartree cube file generated by CP2K
    surface: 1-d int list
      surface is the surface to be calculated
    work_dir: string
      work_dir is the working directory
  Returns:
    v_hartree_file: string
      v_hartree_file contains hartree potential information.
  '''

  line = linecache.getline(cube_file, 3)
  line_split = data_op.split_str(line, ' ')
  atoms_num = int(line_split[0])

  line = linecache.getline(cube_file, 4)
  line_split = data_op.split_str(line, ' ', '\n')
  a_grids = int(line_split[0])
  a = [float(line_split[1]), float(line_split[2]), float(line_split[3])]

  line = linecache.getline(cube_file, 5)
  line_split = data_op.split_str(line, ' ', '\n')
  b_grids = int(line_split[0])
  b = [float(line_split[1]), float(line_split[2]), float(line_split[3])]

  line = linecache.getline(cube_file, 6)
  line_split = data_op.split_str(line, ' ', '\n')
  c_grids = int(line_split[0])
  c = [float(line_split[1]), float(line_split[2]), float(line_split[3])]

  pre_file = 2+4+atoms_num

  if ( surface == [0,0,1] ):
    first_index = a_grids
    second_index = b_grids
    block_line_num = math.ceil(c_grids/6.0)

  if ( surface == [1,0,0] ):
    first_index = b_grids
    second_index = c_grids
    block_line_num = math.ceil(a_grids/6.0)

  if ( surface == [0,1,0] ):
    first_index = a_grids
    second_index = c_grids
    block_line_num = math.ceil(b_grids/6.0)

  v_hartree = np.zeros((a_grids,b_grids,c_grids))

  for i in range(first_index):
    for j in range(second_index):
      for k in range(block_line_num):
        temp_list = []
        line = linecache.getline(cube_file, i*second_index*block_line_num+j*block_line_num+k+pre_file+1)
        line_split = data_op.split_str(line, ' ', '\n')
        for l in range (len(line_split)):
          v_hartree[i,j,k*6+l] = float(line_split[l])

  linecache.clearcache()

  v_hartree_array = np.asfortranarray(v_hartree,dtype='float32')

  if ( surface == [0,0,1] ):
    index_1 = 1
    index_2 = 2
    sum_dim = c_grids
    increment = c[2]/c_grids

  if ( surface == [0,1,0] ):
    index_1 = 1
    index_2 = 3
    sum_dim = b_grids
    increment = b[1]/b_grids

  if ( surface == [1,0,0] ):
    index_1 = 2
    index_2 = 3
    sum_dim = a_grids
    increment = a[0]/b_grids

  v_hartree_surf = statistic_mod.statistic.matrix_element_sum(v_hartree_array, index_1, index_2, sum_dim)

  #Please be careful, the unit of distance in cube file is Bohr.
  v_hartree_file = ''.join((work_dir, '/v_hartree.csv'))
  with open(v_hartree_file, 'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['distance(Bohr)', 'v_hartree(Hartree)'])
    for i in range(c_grids):
      writer.writerow([increment*i, v_hartree_surf[i]])

  return v_hartree_file

def v_hartree_run(hartree_param, work_dir):

  '''
  v_hartree: kernel function to calculate v_hartree

  Args:
    hartree_param: dictionary
      hartree_param contains keywords used in calculating v_hartree.
    work_dir: string
      work_dir is working directory of DPFlow.
  Returns:
    none
  '''

  cube_file = hartree_param['cube_file']
  surface = hartree_param['surface']

  print ('V_HARTREE'.center(80, '*'), flush=True)
  print ('Analyze hartree potential')
  tips = \
'''Tips:
  v_hartree in CP2K = the electrostatic potential generated by nuclei (or ions)
  + the electrostatic potential generated by electrons. The latter is usually
  refereed as hartree potential while the former is refered as an external pote-
  ntial in the literature. In principle, one needs to use v_hartree + v_xc. How-
  ever, v_xc decays much faster than v_hartree so that if electron goes a bit far
  away from a surface, there is only only v_hartree.
  CP2K does not give you the correct fermi level for semiconductor as by default
  it considers the HOMO as the fermi level. So you have to be careful if you are
  working on a semiconductor surface.'''
  print (tips, flush=True)

  v_hartree_file = calc_v_hartree(cube_file, surface, work_dir)

  str_print = 'The hartree potential file is written in %s' %(v_hartree_file)
  print (data_op.str_wrap(str_print, 80), flush=True)
