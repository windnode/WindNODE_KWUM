def get_flow_from_node_names(esys, nodes):
    """Lookup flow in energy system model by node source and target names

    Parameters
    ----------
    esys : :class:`oemof.solph.EnergySystem`
        Energy system model
    nodes : :obj:`tuple` of :obj:`str`
        Tuple in format (node_source, node_target)

    Returns
    -------
    :class:`oemof.solph.Flow`
    """
    for (source, target) in esys.flows():
        if (str(source), str(target)) == nodes:
            return esys.flows()[source, target]
    raise ValueError('Flow cannot be found in energy system!')
