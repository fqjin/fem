def test_write_pml_elems(tmpdir, sorted_elems):
    from fem.mesh.bc import write_pml_elems

    f = tmpdir.join("elems_pml.dyn")
    write_pml_elems(sorted_elems, pmlfile=f.strpath)
    lines = f.readlines()
    assert lines[0][0] == "$"
    assert lines[1] == "*ELEMENT_SOLID\n"
    assert lines[2] == "1,1,1,2,13,12,122,123,134,133\n"
    assert lines[-2] == "1000,1,1198,1199,1210,1209,1319,1320,1331,1330\n"
    assert lines[-1] == "*END\n"


def test_assign_node_constraints(nodeIDcoords):
    from fem.mesh.fem_mesh import SortNodeIDs
    from fem.mesh.bc import assign_node_constraints
    [snic, axes] = SortNodeIDs(nodeIDcoords, sort=False)
    face_constraints = (('1,1,1,1,1,1', '2,2,2,2,2,2'),
                        ('3,3,3,3,3,3', '4,4,4,4,4,4'),
                        ('5,5,5,5,5,5', '6,6,6,6,6,6'))
    bcdict = assign_node_constraints(snic, axes, face_constraints)

    assert bcdict[1] == '5,5,5,5,5,5'


def test_assign_edge_sym_constraints(nodeIDcoords):
    from fem.mesh.fem_mesh import SortNodeIDs
    from fem.mesh.bc import assign_edge_sym_constraints
    [snic, axes] = SortNodeIDs(nodeIDcoords, sort=False)
    bcdict = {}
    edge_constraints = (((0, 1), (1, 0), (0, 0)), '1,1,0,1,1,1')
    bcdict = assign_edge_sym_constraints(bcdict, snic, axes, edge_constraints)

    for nodeID in (737, 616, 495, 374):
        assert bcdict[nodeID] == "1,1,0,1,1,1"


def test_exclude_zminmax_edge_sym_constraints(nodeIDcoords):
    from fem.mesh.fem_mesh import SortNodeIDs
    from fem.mesh.bc import assign_edge_sym_constraints
    [snic, axes] = SortNodeIDs(nodeIDcoords, sort=False)
    bcdict = {}
    edge_constraints = (((0, 1), (1, 0), (0, 0)), '1,1,0,1,1,1')
    bcdict = assign_edge_sym_constraints(bcdict, snic, axes, edge_constraints)

    for nodeID in (1221, 11):
        assert nodeID not in bcdict.keys()


def test_constrain_sym_pml_nodes(nodeIDcoords):
    """THIS FUNCTION IS NOT NEEDED!!
    """
    from fem.mesh.fem_mesh import SortNodeIDs
    from fem.mesh.bc import constrain_sym_pml_nodes
    [snic, axes] = SortNodeIDs(nodeIDcoords, sort=False)
    bcdict = {}
    edge_constraints = (((0, 1), (1, 0), (0, 0)), '1,1,0,1,1,1')
    pml_elems = ((3, 0), (0, 1), (2, 3))
    bcdict = constrain_sym_pml_nodes(bcdict, snic, axes, pml_elems,
                                     edge_constraints)
    # check x sym face
    for start_node in (11, 132, 253, 858, 979, 1100, 1221):
        for nodeID in range(start_node, start_node + 111, 11):
            assert bcdict[nodeID] == '1,1,1,1,1,1'
    for not_in_bc in (374, 495, 616, 737):
        assert not_in_bc not in bcdict.keys()
    # check y sym face
    for start_node in (1, 122, 243, 848, 969, 1090, 1211):
        for nodeID in range(start_node, start_node + 11):
            assert bcdict[nodeID] == '1,1,1,1,1,1'


def test_assign_pml_elems(sorted_elems):
    from fem.mesh.bc import assign_pml_elems

    pml_elems = ((3, 0), (0, 1), (2, 3))

    sorted_pml_elems = assign_pml_elems(sorted_elems, pml_elems)

    # check the xmin face
    assert sorted_pml_elems[sorted_pml_elems['id'] == 1]['pid'] == 2
    assert sorted_pml_elems[sorted_pml_elems['id'] == 2]['pid'] == 2
    assert sorted_pml_elems[sorted_pml_elems['id'] == 3]['pid'] == 2
    assert sorted_pml_elems[sorted_pml_elems['id'] == 4]['pid'] == 2
    assert sorted_pml_elems[sorted_pml_elems['id'] == 91]['pid'] == 2
    assert sorted_pml_elems[sorted_pml_elems['id'] == 92]['pid'] == 2
    assert sorted_pml_elems[sorted_pml_elems['id'] == 93]['pid'] == 2
    assert sorted_pml_elems[sorted_pml_elems['id'] == 94]['pid'] == 2
    assert sorted_pml_elems[sorted_pml_elems['id'] == 901]['pid'] == 2
    assert sorted_pml_elems[sorted_pml_elems['id'] == 902]['pid'] == 2
    assert sorted_pml_elems[sorted_pml_elems['id'] == 903]['pid'] == 2
    assert sorted_pml_elems[sorted_pml_elems['id'] == 904]['pid'] == 2
    assert sorted_pml_elems[sorted_pml_elems['id'] == 991]['pid'] == 2
    assert sorted_pml_elems[sorted_pml_elems['id'] == 992]['pid'] == 2
    assert sorted_pml_elems[sorted_pml_elems['id'] == 993]['pid'] == 2
    assert sorted_pml_elems[sorted_pml_elems['id'] == 994]['pid'] == 2

    # check the ymax face
    assert sorted_pml_elems[sorted_pml_elems['id'] == 95]['pid'] == 2
    assert sorted_pml_elems[sorted_pml_elems['id'] == 100]['pid'] == 2
    assert sorted_pml_elems[sorted_pml_elems['id'] == 995]['pid'] == 2
    assert sorted_pml_elems[sorted_pml_elems['id'] == 1000]['pid'] == 2

    # check the zmax face
    assert sorted_pml_elems[sorted_pml_elems['id'] == 910]['pid'] == 2
    assert sorted_pml_elems[sorted_pml_elems['id'] == 810]['pid'] == 2
    assert sorted_pml_elems[sorted_pml_elems['id'] == 710]['pid'] == 2
    assert sorted_pml_elems[sorted_pml_elems['id'] == 610]['pid'] == 1

    # check the zmin face
    assert sorted_pml_elems[sorted_pml_elems['id'] == 10]['pid'] == 2
    assert sorted_pml_elems[sorted_pml_elems['id'] == 110]['pid'] == 2
    assert sorted_pml_elems[sorted_pml_elems['id'] == 210]['pid'] == 1


def test_write_bc(tmpdir):
    from fem.mesh.bc import write_bc
    bcdict = {1: '1,1,1,0,0,0', 2: '0,1,0,0,1,0'}
    f = tmpdir.join("bc.dyn")
    write_bc(bcdict, bc=f.strpath)
    lines = f.readlines()
    assert lines[1] == "*BOUNDARY_SPC_NODE\n"
    assert lines[2] == "1,0,1,1,1,0,0,0\n"
    assert lines[3] == "2,0,0,1,0,0,1,0\n"
    assert lines[4] == "*END\n"

    return 0


def test_read_cli():
    from fem.mesh.bc import read_cli
    import sys

    sys.argv = ['bc.py', '--nonreflect']
    opts = read_cli()

    assert opts.nonreflect is True
    assert opts.pml is False

    sys.argv = ['bc.py', '--pml']
    opts = read_cli()

    assert opts.nonreflect is False
    assert opts.pml is True
    assert opts.num_pml_elems == 5
    assert opts.nodefile == "nodes.dyn"
    assert opts.elefile == "elems.dyn"
    assert opts.bcfile == "bc.dyn"
    assert opts.sym == "q"
    assert opts.pml_partID == 2

    sys.argv = ['bc.py', '--pml', '--num_pml_elems', '8']
    opts = read_cli()
    assert opts.num_pml_elems == 8
    assert opts.num_pml_elems != 5
