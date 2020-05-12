# Copyright 2019 D-Wave Systems Inc.
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

import dwavebinarycsp
from hybrid.reference.kerberos import KerberosSampler

from utilities import visualize_map

class State:
    def __init__(self, name):
        self.name = name
        self.red = name + "_r"
        self.green = name + "_g"
        self.blue = name + "_b"
        self.yellow = name + "_y"

# Set up states
al = State("al")	# Alabama
az = State("az")	# Arizona
ar = State("ar")	# Arkansas
ca = State("ca")	# California
co = State("co")	# Colorado
ct = State("ct")	# Connecticut
de = State("de")	# Delaware
fl = State("fl")	# Florida
ga = State("ga")	# Georgia
id = State("id")	# Idaho
il = State("il")	# Illinois
ind = State("in")	# Indiana
ia = State("ia")	# Iowa
ks = State("ks")	# Kansas
ky = State("ky")	# Kentucky
la = State("la")	# Louisiana
me = State("me")	# Maine
md = State("md")	# Maryland
ma = State("ma")	# Massachusetts
mi = State("mi")	# Michigan
mn = State("mn")	# Minnesota
ms = State("ms")	# Mississippi
mo = State("mo")	# Missouri
mt = State("mt")	# Montana
ne = State("ne")	# Nebraska
nv = State("nv")	# Nevada
nh = State("nh")	# New Hampshire
nj = State("nj")	# New Jersey
nm = State("nm")	# New Mexico
ny = State("ny")	# New York
nc = State("nc")	# North Carolina
nd = State("nd")	# North Dakota
oh = State("oh")	# Ohio
ok = State("ok")	# Oklhahoma
ore = State("or")	# Oregon
pa = State("pa")	# Pennsylvania
ri = State("ri")	# Rhode Island
sc = State("sc")	# South Carolina
sd = State("sd")	# South Dakota
tn = State("tn")	# Tennesse
tx = State("tx")	# Texas
ut = State("ut")	# Utah
vt = State("vt")	# Vermont
va = State("va")	# Virginia
wa = State("wa")	# Washington
wv = State("wv")	# West Virginia
wi = State("wi")	# Wisconsin
wy = State("wy")	# Wyoming

states = [al, az, ar, ca, co, ct, de, fl, ga, id, il, ind, ia, ks, ky, la, me, md, ma, mi, mn, ms, mo, mt, ne, nv, nh, nj, nm, ny, nc, nd, oh, ok, ore, pa, ri, sc, sd, tn, tx, ut, vt, va, wa, wv, wi, wy]


# Set up state neighbours (i.e. shares a border)
neighbours = [(al, fl),
              (al, ga),
              (al, mi),
              (al, tn),
              (az, ca),
              (az, co),
              (az, nv),
              (az, nm),
              (az, ut),
              (ar, la),
              (ar, mi),
              (ar, mo),
              (ar, ok),
              (ar, tn),
              (ar, tx),
              (ca, nv),
              (ca, ore),
              (co, ks),
              (co, ne),
              (co, nm),
              (co, ok),
              (co, ut),
              (co, wy),
              (ct, ma),
              (ct, ny),
              (ct, ri),
              (de, md),
              (de, nj),
              (de, pa),
              (fl, ga),
              (ga, nc),
              (ga, sc),
              (ga, tn),
              (id, mt),
              (id, nv),
              (id, ore),
              (id, ut),
              (id, wy),
              (il, ind),
              (il, ia),
              (il, ky),
              (il, mi),
              (il, mo),
              (il, wi),
              (ind, ky),
              (ind, mi),
              (ind, oh),
              (ia, mn),
              (ia, mo),
              (ia, ne),
              (ia, sd),
              (ia, wi),
              (ks, mo),
              (ks, ne),
              (ks, ok),
              (ky, mo),
              (ky, oh),
              (ky, tn),
              (ky, va),
              (ky, wv),
              (la, ms),
              (la, tx),
              (me, nh),
              (md, pa),
              (md, va),
              (md, wv),
              (ma, nh),
              (ma, ny),
              (ma, ri),
              (ma, vt),
              (mi, mn),
              (mi, oh),
              (mi, wi),
              (mn, nd),
              (mn, sd),
              (mn, wi),
              (ms, tn),
              (mo, ne),
              (mo, ok),
              (mo, tn),
              (mt, nd),
              (mt, sd),
              (mt, wy),
              (ne, sd),
              (ne, wy),
              (nv, ore),
              (nv, ut),
              (nh, vt),
              (nj, ny),
              (nj, pa),
              (nm, ok),
              (nm, tx),
              (nm, ut),
              (ny, pa),
              (ny, ri),
              (ny, vt),
              (nc, sc),
              (nc, tn),
              (nv, va),
              (nd, sd),
              (oh, pa),
              (oh, wv),
              (ok, tx),
              (ore, wa),
              (pa, wv),
              (sd, wy),
              (tn, va),
              (ut, wy),
              (va, wv)]

# Initialize constraint satisfaction problem
csp = dwavebinarycsp.ConstraintSatisfactionProblem(dwavebinarycsp.BINARY)
not_both = {(0, 1), (1, 0), (0, 0)}
select_one = {(0, 0, 0, 1),
              (0, 0, 1, 0),
              (0, 1, 0, 0),
              (1, 0, 0, 0)}

# Apply one color constraint
for p in states:
    csp.add_constraint(select_one, {p.red, p.green, p.blue, p.yellow})

# Apply no color sharing between neighbours
for x, y in neighbours:
    csp.add_constraint(not_both, {x.red, y.red})
    csp.add_constraint(not_both, {x.green, y.green})
    csp.add_constraint(not_both, {x.blue, y.blue})
    csp.add_constraint(not_both, {x.yellow, y.yellow})

# Combine constraints to form a BQM
bqm = dwavebinarycsp.stitch(csp)

# Solve BQM
solution = KerberosSampler().sample(bqm)
best_solution = solution.first.sample
print("Solution: ", best_solution)

# Verify
is_correct = csp.check(best_solution)
print("Does solution satisfy our constraints? {}".format(is_correct))


# Visualize the solution
# Note: The following is purely for visualizing the output and is not necessary
# for the demo.

nodes = [u.name for u in states]
edges = [(u.name, v.name) for u, v in neighbours]
visualize_map(nodes, edges, best_solution)

