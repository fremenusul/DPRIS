def rankBuilder(rank):
    if rank == 'PV2':
        return 'PFC'
    elif rank == 'PFC':
        return 'SPC'
    elif rank == 'SPC':
        return 'CPL'
    elif rank == 'CPL':
        return 'SGT'
    elif rank == 'SGT':
        return 'SSG'
    elif rank == 'SSG':
        return 'SFC'
    elif rank == 'SFC':
        return 'MSG'
    elif rank == 'MSG':
        return '1SG'
    elif rank == '1SG':
        return 'SGM'
    elif rank == 'SGM':
        return 'CSM'
    elif rank == 'CSM':
        return '2LT'
    elif rank == '2LT':
        return '1LT'
    elif rank == '1LT':
        return 'CPT'
    elif rank == 'CPT':
        return 'MAJ'
    elif rank == 'MAJ':
        return 'LTC'

def rankBuilderW(rank):
    if rank == 'PV2':
        return 'WOC'
    elif rank == 'WOC':
        return 'WO1'
    elif rank == 'WO1':
        return 'CW2'
    elif rank == 'CW2':
        return 'CW3'
    elif rank == 'CW3':
        return 'CW4'
    elif rank == 'CW4':
        return 'CW5'

def rankDemote(rank):
    if rank == 'LTC':
        return 'MAJ'
    elif rank == 'MAJ':
        return 'CPT'
    elif rank == 'CPT':
        return '1LT'
    elif rank == '1LT':
        return '2LT'
    elif rank == '2LT':
        return 'CSM'
    elif rank == 'CSM':
        return 'SGM'
    elif rank == 'SGM':
        return '1SG'
    elif rank == '1SG':
        return 'MSG'
    elif rank == 'MSG':
        return 'SFC'
    elif rank == 'SFC':
        return 'SSG'
    elif rank == 'SSG':
        return 'SGT'
    elif rank == 'SGT':
        return 'CPL'
    elif rank == 'CPL':
        return 'SPC'
    elif rank == 'SPC':
        return 'PFC'
    elif rank == 'PFC':
        return 'PV2'
    elif rank == 'PV2':
        return 'RCT'

def rankDemoteW(rank):
    if rank == 'CW5':
        return 'CW4'
    elif rank == 'CW4':
        return 'CW3'
    elif rank == 'CW3':
        return 'CW2'
    elif rank == 'CW2':
        return 'WO1'
    elif rank == 'WO1':
        return 'WOC'
    elif rank == 'WOC':
        return 'PV2'