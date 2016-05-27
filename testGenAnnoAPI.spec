module testGenAnnoAPI {

typedef string ObjectReference;

typedef structure {
    /** The identifier for the contig to which this region corresponds. */
     string contig_id;
    /** Either a "+" or a "-", for the strand on which the region is located. */
     string strand;
    /** Starting position for this region. */
     int start;
    /** Distance from the start position that bounds the end of the region. */
     int length;
}  Region;

/**
 * Filters passed to :meth:`get_feature_ids`
 */
typedef structure {
    /**
     * List of Feature type strings.
     */
     list<string> type_list;
    /**
     * List of region specs.
     * For example::
     *     [{"contig_id": str, "strand": "+"|"-",
     *       "start": int, "length": int},...]
     *
     * The Feature sequence begin and end are calculated as follows:
     *   - [start, start) for "+" strand
     *   - (start - length, start] for "-" strand
     */
     list<Region> region_list;
    /**
     * List of function strings.
     */
     list<string> function_list;
    /**
     *  List of alias strings.
     */
     list<string> alias_list;
}  Feature_id_filters;

typedef structure {
    /** Mapping of Feature type string to a list of Feature IDs */
     mapping<string, list<string>> by_type;
    /**
     * Mapping of contig ID, strand "+" or "-", and range "start--end" to
     * a list of Feature IDs. For example::
     *    {'contig1': {'+': {'123--456': ['feature1', 'feature2'] }}}
     */
     mapping<string, mapping<string, mapping<string, list<string>>>> by_region;
    /** Mapping of function string to a list of Feature IDs */
     mapping<string, list<string>> by_function;
    /** Mapping of alias string to a list of Feature IDs */
     mapping<string, list<string>> by_alias;
}  Feature_id_mapping;

typedef structure {
    /** Identifier for this feature */
     string feature_id;
    /** The Feature type e.g., "mRNA", "CDS", "gene", ... */
     string feature_type;
    /** The functional annotation description */
     string feature_function;
    /** Dictionary of Alias string to List of source string identifiers */
     mapping<string, list<string>> feature_aliases;
    /** Integer representing the length of the DNA sequence for convenience */
     int feature_dna_sequence_length;
    /** String containing the DNA sequence of the Feature */
     string feature_dna_sequence;
    /** String containing the MD5 of the sequence, calculated from the uppercase string */
     string feature_md5;
    /**
     * List of dictionaries::
     *     { "contig_id": str,
     *       "start": int,
     *       "strand": str,
     *       "length": int  }
     *
     * List of Feature regions, where the Feature bounds are
     * calculated as follows:
     *
     * - For "+" strand, [start, start + length)
     * - For "-" strand, (start - length, start]
    */
     list<Region> feature_locations;
    /**
     * List of any known publications related to this Feature
     */
     list<string> feature_publications;
    /**
     * List of strings indicating known data quality issues.
     * Note: not used for Genome type, but is used for
     * GenomeAnnotation
     */
     list<string> feature_quality_warnings;
    /**
     * Quality value with unknown algorithm for Genomes,
     * not calculated yet for GenomeAnnotations.
     */
     list<string> feature_quality_score;
    /** Notes recorded about this Feature */
     string feature_notes;
    /** Inference information */
     string feature_inference;
}  Feature_data;

typedef structure {
    /** Protein identifier, which is feature ID plus ".protein" */
     string protein_id;
    /** Amino acid sequence for this protein */
     string protein_amino_acid_sequence;
    /** Function of protein */
     string protein_function;
    /** List of aliases for the protein */
     list<string> protein_aliases;
    /** MD5 hash of the protein translation (uppercase) */
     string protein_md5;
     list<string> protein_domain_locations;
}  Protein_data;

typedef structure {
    /** Location of the exon in the contig. */
     Region exon_location;
    /** DNA Sequence string. */
     string exon_dna_sequence;
    /** The position of the exon, ordered 5' to 3'. */
     int exon_ordinal;
}  Exon_data;

typedef structure {
    /** Locations of this UTR */
     list<Region> utr_locations;
    /** DNA sequence string for this UTR */
     string utr_dna_sequence;
}  UTR_data;


    /**
     * Retrieve the Taxon associated with this GenomeAnnotation.
     *
     * @return Reference to TaxonAPI object
     */
     funcdef get_taxon( ObjectReference ref)  returns (ObjectReference) authentication required;

    /**
     * Retrieve the Assembly associated with this GenomeAnnotation.
     *
     * @return Reference to AssemblyAPI object
     */
     funcdef get_assembly( ObjectReference ref)  returns (ObjectReference) authentication required;

    /**
     * Retrieve the list of Feature types.
     *
     * @return List of feature type identifiers (strings)
     */
     funcdef get_feature_types( ObjectReference ref)  returns (list<string>) authentication required;

    /**
     * Retrieve the descriptions for each Feature type in
     * this GenomeAnnotation.
     *
     * @param feature_type_list List of Feature types. If this list
     *  is empty or None,
     *  the whole mapping will be returned.
     * @return Name and description for each requested Feature Type
     */
     funcdef get_feature_type_descriptions( ObjectReference ref,
                                                     list<string> feature_type_list)  returns (mapping<string,string>) authentication required;

    /**
     * Retrieve the count of each Feature type.
     *
     * @param feature_type_list  List of Feature Types. If empty,
     *   this will retrieve  counts for all Feature Types.
     */
     funcdef get_feature_type_counts( ObjectReference ref,
                                            list<string> feature_type_list)  returns (mapping<string,int>) authentication required;

    /**
     * Retrieve Feature IDs, optionally filtered by type, region, function, alias.
     *
     * @param filters Dictionary of filters that can be applied to contents.
     *   If this is empty or missing, all Feature IDs will be returned.
     * @param group_type How to group results, which is a single string matching one
     *   of the values for the ``filters`` parameter.
     * @return Grouped mapping of features.
     */
     funcdef get_feature_ids( ObjectReference ref,
                                       Feature_id_filters filters,
                                       string group_type)  returns (Feature_id_mapping) authentication required;

    /**
     * Retrieve Feature data.
     *
     * @param feature_id_list List of Features to retrieve.
     *   If None, returns all Feature data.
     * @return Mapping from Feature IDs to dicts of available data.
     */
     funcdef get_features( ObjectReference ref,
                                           list<string> feature_id_list)  returns (mapping<string, Feature_data>) authentication required;

    /**
     * Retrieve Protein data.
     *
     * @return Mapping from protein ID to data about the protein.
     */
     funcdef get_proteins( ObjectReference ref)  returns (mapping<string, Protein_data>) authentication required;

    /**
     * Retrieve Feature locations.
     *
     * @param feature_id_list List of Feature IDs for which to retrieve locations.
     *     If empty, returns data for all features.
     * @return Mapping from Feature IDs to location information for each.
     */
     funcdef get_feature_locations( ObjectReference ref,
                                                    list<string> feature_id_list)  returns (mapping<string, list<Region>>) authentication required;

    /**
     * Retrieve Feature publications.
     *
     * @param feature_id_list List of Feature IDs for which to retrieve publications.
     *     If empty, returns data for all features.
     * @return Mapping from Feature IDs to publication info for each.
     */
     funcdef get_feature_publications( ObjectReference ref,
                                                      list<string> feature_id_list)  returns (mapping<string,list<string>>) authentication required;

    /**
     * Retrieve Feature DNA sequences.
     *
     * @param feature_id_list List of Feature IDs for which to retrieve sequences.
     *     If empty, returns data for all features.
     * @return Mapping of Feature IDs to their DNA sequence.
     */
     funcdef get_feature_dna( ObjectReference ref,
                                       list<string> feature_id_list)  returns (mapping<string,string>) authentication required;

    /**
     * Retrieve Feature functions.
     *
     * @param feature_id_list List of Feature IDs for which to retrieve functions.
     *     If empty, returns data for all features.
     * @return Mapping of Feature IDs to their functions.
     */
     funcdef get_feature_functions( ObjectReference ref,
                                             list<string> feature_id_list)  returns (mapping<string,string>) authentication required;

    /**
     * Retrieve Feature aliases.
     *
     * @param feature_id_list List of Feature IDS for which to retrieve aliases.
     *     If empty, returns data for all features.
     * @return Mapping of Feature IDs to a list of aliases.
     */
     funcdef get_feature_aliases( ObjectReference ref,
                                                 list<string> feature_id_list)  returns (mapping<string,list<string>>) authentication required;

    /**
     * Retrieves coding sequence Features (cds) for given gene Feature IDs.
     *
     * @param feature_id_list List of gene Feature IDS for which to retrieve CDS.
     *     If empty, returns data for all features.
     * @return Mapping of gene Feature IDs to a list of CDS Feature IDs.
     */
     funcdef get_cds_by_gene( ObjectReference ref,
                                             list<string> gene_id_list)  returns (mapping<string,list<string>>) authentication required;

    /**
     * Retrieves coding sequence (cds) Feature IDs for given mRNA Feature IDs.
     *
     * @param feature_id_list List of mRNA Feature IDS for which to retrieve CDS.
     *     If empty, returns data for all features.
     * @return Mapping of mRNA Feature IDs to a list of CDS Feature IDs.
     */
     funcdef get_cds_by_mrna( ObjectReference ref,
                                       list<string> mrna_id_list)  returns (mapping<string,string>) authentication required;

    /**
     * Retrieves gene Feature IDs for given coding sequence (cds) Feature IDs.
     *
     * @param feature_id_list List of cds Feature IDS for which to retrieve gene IDs.
     *     If empty, returns all cds/gene mappings.
     * @return Mapping of cds Feature IDs to gene Feature IDs.
     */
     funcdef get_gene_by_cds( ObjectReference ref,
                                       list<string> cds_id_list)  returns (mapping<string,string>) authentication required;

    /**
     * Retrieves gene Feature IDs for given mRNA Feature IDs.
     *
     * @param feature_id_list List of mRNA Feature IDS for which to retrieve gene IDs.
     *     If empty, returns all mRNA/gene mappings.
     * @return Mapping of mRNA Feature IDs to gene Feature IDs.
     */
     funcdef get_gene_by_mrna( ObjectReference ref,
                                        list<string> mrna_id_list)  returns (mapping<string,string>) authentication required;

    /**
     * Retrieves mRNA Features for given coding sequences (cds) Feature IDs.
     *
     * @param feature_id_list List of cds Feature IDS for which to retrieve mRNA IDs.
     *     If empty, returns all cds/mRNA mappings.
     * @return Mapping of cds Feature IDs to mRNA Feature IDs.
     */
     funcdef get_mrna_by_cds( ObjectReference ref,
                                       list<string> cds_id_list)  returns (mapping<string,string>) authentication required;

    /**
     * Retrieve the mRNA IDs for given gene IDs.
     *
     * @param feature_id_list List of gene Feature IDS for which to retrieve mRNA IDs.
     *     If empty, returns all gene/mRNA mappings.
     * @return Mapping of gene Feature IDs to a list of mRNA Feature IDs.
     */
     funcdef get_mrna_by_gene( ObjectReference ref,
                                               list<string> gene_id_list)  returns (mapping<string, list<string>>) authentication required;

    /**
     * Retrieve Exon information for each mRNA ID.
     *
     * @param feature_id_list List of mRNA Feature IDS for which to retrieve exons.
     *     If empty, returns data for all exons.
     * @return Mapping of mRNA Feature IDs to a list of exons (:js:data:`Exon_data`).
     */
     funcdef get_mrna_exons( ObjectReference ref,
                                                list<string> mrna_id_list)  returns (mapping<string, list<Exon_data>>) authentication required;

    /**
     * Retrieve UTR information for each mRNA Feature ID.
     *
     *  UTRs are calculated between mRNA features and corresponding CDS features.
     *  The return value for each mRNA can contain either:
     *     - no UTRs found (empty dict)
     *     -  5' UTR only
     *     -  3' UTR only
     *     -  5' and 3' UTRs
     *
     *  Note: The Genome data type does not contain interfeature
     *  relationship information. Calling this method for Genome objects
     *  will raise a :js:throws:`exc.TypeException`.
     *
     * @param feature_id_list List of mRNA Feature IDS for which to retrieve UTRs.
     * If empty, returns data for all UTRs.
     * @return Mapping of mRNA Feature IDs to a mapping that contains
     * both 5' and 3' UTRs::
     *     { "5'UTR": :js:data:`UTR_data`, "3'UTR": :js:data:`UTR_data` }
     */
     funcdef get_mrna_utrs( ObjectReference ref,
                                                     list<string> mrna_id_list)  returns (mapping<string, mapping<string, UTR_data>>) authentication required;

};
