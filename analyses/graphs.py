# coding: utf-8

# Copyright 2022, Robert Dyer,
#                 and University of Nebraska Board of Regents
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from matplotlib import pyplot as plt

__all__ = ["setup_plots"]

def setup_plots():
    plt.rcParams['figure.figsize'] = [6.0, 5.0]
    plt.rcParams['figure.dpi'] = 600.0
    plt.rcParams['font.size'] = 24
    plt.subplots(constrained_layout=True)
