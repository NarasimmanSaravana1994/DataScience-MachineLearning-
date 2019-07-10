am_DucenApp.controller('ac_TextModelling',
['$scope', '$rootScope', 'as_Session', 'as_AnalysisService', 'as_Utilities', 'as_UnifiedEngine', 'as_GlobalSettings', '$state', '$compile', '$timeout',
function (p_scope, p_rootScope, as_Session, as_AnalysisService, as_Utilities, as_UnifiedEngine, as_GlobalSettings, p_state, p_compile, p_timeout) {

    p_scope.cs_AssosiatedDataset = {
        selectedDatasetId: '',
        Datasources: [],
        Dataset: {},
        l_gridOptions: {},
        DropDownDataSources: [],
        OwnerInfo: {
            UserId: as_Session.fn_GetSession("CurrentUserSession").UserId,
            CustomerId: as_Session.fn_GetSession("CurrentUserSession").CustomerId,
            GroupId: as_Session.fn_GetSession("CurrentUserSession").UserGroupId,
            UserRoleId: as_Session.fn_GetSession("CurrentUserSession").UserRoleId,
            Language: as_Session.fn_GetSession("CurrentUserSession").Language
        }
    }
    p_scope.cs_AnalysisModel = {
        AssosiatedDataset:''
    };
   // p_scope.cs_AssosiatedDataset.selectedDatasetId = '';
    p_scope.getalldata = function () {
        var l_objParam = {
            UserDetails: p_rootScope.fn_GetUserDetails(true),
            SelectedDatasets: ""
        };
        as_AnalysisService.fn_GetDatasourcesForAnalytics(l_objParam).success(function (l_objResult) {           

            p_scope.cs_AssosiatedDataset.Datasources = l_objResult;
            p_scope.cs_AssosiatedDataset.DropDownDataSources = p_scope.fn_GetDropDownSource(p_scope.cs_AssosiatedDataset.Datasources, 'Id', 'Name').Data;
            
        }).error(function (ex) {

        });
    };
    p_scope.getalldata();
    p_scope.fn_GetDropDownSource = function (p_strObject, p_strValueFeild, p_strTextFeild) {
        var l_strValueProperty = p_strValueFeild;
        var l_strTextProperty = p_strTextFeild;
        if (p_strTextFeild == undefined || p_strTextFeild == "") {
            l_strTextProperty = p_strValueFeild;
        }
        var l_objdataset = $.map(p_strObject, function (value) {
            return {
                Value: value[l_strValueProperty], Text: value[l_strTextProperty]
            };
        });
        return {
            Data: l_objdataset
        };
       
    }

    p_scope.fn_RenderPreviewGrid= function () {
        //alert("22")
        if (p_scope.cs_AssosiatedDataset.selectedDatasetId == '') {
            cs_toolkit.fn_ShowStatus({
                message: as_Utilities.fn_GetLabel(4612), type: "error"
            });
            return;
        }
        cs_toolkit.fn_BlockUILoader({
            action: 'show', target: "#previewUI", message: as_Utilities.fn_GetLabel(3784)
        });
        $('#divAssociatedDatsetPreview').modal();
        Metronic.blockUI({
            target: $('#divAssociatedDatsetPreview .portlet-body'),
            animate: true,
            overlayColor: '#333'
        });
        var l_previewColumns = "";
       
        if (p_scope.cs_AssosiatedDataset.Dataset.DatasetType == '15') {
            var l_ColumnsIncluded = p_scope.cs_Common.fn_GetOLAPPreviewColumns();
            l_previewColumns = l_ColumnsIncluded.join(",");
        }
        // This service call will execute the selected datset query and returns the top 10 records to render preview grid 
        as_AnalysisService.fn_PreviewDataset({
            UserDetails: p_rootScope.fn_GetUserDetails(false),
            DatasetInfo: {
                DatasetXML: p_scope.cs_AssosiatedDataset.Dataset.Xml
            },
            SelectedColumns: l_previewColumns
        }).success(function (p_data) {
            if (p_data != null) {
                Metronic.unblockUI($('#divAssociatedDatsetPreview .portlet-body'));
                var l_datasource = p_data.PreviewData.Items;
                var l_arrColumns = [];
                var l_columns = [];
                if (p_scope.cs_AssosiatedDataset.Dataset.DatasetType == '15') {
                    $(p_scope.cs_AssosiatedDataset.Dataset.CombinedColumns).each(function () {
                        if ($.inArray(this.Id, l_ColumnsIncluded) != -1) {
                            l_columns.push(this);
                        }
                    });
                    /* To bind the olap columns in ui-grid while preview the data*/
                    $(l_datasource).each(function () {
                        for (var key in this) {
                            var value = this[key];
                            delete this[key]
                            key = key.split('.')[1].replace(/[[\]]/g, '');
                            this[key] = value;
                        }
                    });
                }
                else {
                    l_columns = JSON.parse(angular.toJson(p_scope.cs_AssosiatedDataset.Dataset.CombinedColumns));
                }
                $(l_columns).each(function () {
                    l_arrColumns.push({
                        field: p_scope.cs_AssosiatedDataset.Dataset.DatasetType == '15' ? this.DisplayName : this.Name,
                        type: this.Type || this.DBType,
                        displayName: this.DisplayName,
                        minWidth: 200,
                        fullDetail: this
                    });
                });
                p_scope.cs_AssosiatedDataset.l_gridOptions.columnDefs = l_arrColumns;
                p_scope.cs_AssosiatedDataset.l_gridOptions.data = l_datasource;
                p_scope.cs_AssosiatedDataset.l_gridOptions.enableHorizontalScrollbar = true;
                p_scope.cs_AssosiatedDataset.l_gridOptions.enableVerticalScrollbar = true;
                p_scope.cs_AssosiatedDataset.l_gridOptions.enableSorting = false;
                p_scope.cs_AssosiatedDataset.l_gridOptions.enableColumnMenus = false;
            }
            p_scope.cs_AssosiatedDataset.l_gridOptions.HasError = false;
            if ($.browser.safari || $.browser.msie) setTimeout(function () {
                $(".ui-grid-viewport").scroll();
            }, 100);
            cs_toolkit.fn_BlockUILoader({
                action: 'hide', target: "#previewUI", message: as_Utilities.fn_GetLabel(3784)
            });
        }).error(function (e) {
            cs_toolkit.fn_BlockUILoader({
                action: 'hide', target: "#previewUI", message: as_Utilities.fn_GetLabel(3784)
            });
            p_scope.cs_AssosiatedDataset.l_gridOptions.HasError = true;
            p_scope.cs_AssosiatedDataset.l_gridOptions.ErrorMessaage = e.InnerException.ExceptionMessage;
        });
    }
 
    

    p_scope.fn_GetDatasetInfo = function (p_previewDatasetId) {
        //alert("23")
  
        //var fn_ConfirmGetDatasetInfo = function () {
           
            p_scope.cs_AnalysisModel.AssosiatedDataset = p_previewDatasetId;
            p_scope.fn_LoadDataset (function (p_objResult) {
                var isResetAnalysisModel = false;
                if (p_objResult.length != 0) {
                    $(p_objResult).each(function () {
                        p_scope.cs_AssosiatedDataset.Dataset = p_objResult[0];
                        //p_scope.cs_EDADataset.AssociatedColumns = p_scope.cs_Common.fn_GetDropDownSource(p_scope.cs_AssosiatedDataset.Dataset.CombinedColumns, 'Id', 'Name').Data;
                        isResetAnalysisModel = true;
                    });
                }
                /* Initializing the AnalysisModel when selected datset is changed */
                //if (isResetAnalysisModel) {
                //    p_scope.cs_AnalysisModel.EDADataset.Columns = [];
                //    p_scope.cs_AnalysisModel.EDADataset.AnalysisType = '1';
                //    p_scope.cs_AnalysisModel.EDADataset.FilterConfig.expression = as_Utilities.fn_GetLabel(90027);
                //    p_scope.cs_AnalysisModel.EDADataset.FilterConfig.values = {};
                //    p_scope.cs_AnalysisModel.TrainedModels = [];
                //    p_scope.cs_AnalysisModel.ProblemStatement = '';
                //    p_scope.cs_Common.selectedTab = 1;
                //}
                cs_toolkit.fn_BlockUILoader({ action: 'hide', target: "#divMain", message: as_Utilities.fn_GetLabel(3784) });
            });
       // }
        //if (p_scope.cs_AnalysisModel.AssosiatedDataset != '' && p_previewDatasetId != '') {
        //    var l_boolIsChanged = p_scope.cs_Common.fn_TrackChanges();
        //    if (l_boolIsChanged) {
        //        var l_param = {
        //            title: as_Utilities.fn_GetLabel(335),
        //            message: "Dataset has been changed, EDA and Model details would be lost. Do you want to continue?",
        //            fn_OnConfirmation: fn_ConfirmGetDatasetInfo,
        //            fn_OnCancel: function () {
        //                p_scope.cs_AssosiatedDataset.selectedDatasetId = p_scope.cs_AnalysisModel.AssosiatedDataset;
        //                $('.clsConfirmationBox').modal('hide');
        //            }
        //        };
        //        cs_toolkit.fn_Confirmation(l_param);
        //    }
        //    else {
        //        fn_ConfirmGetDatasetInfo();
        //    }
        //}
        //else {
        //    fn_ConfirmGetDatasetInfo();
        //}
    }

    p_scope.fn_LoadDataset = function (p_callback) {
        cs_toolkit.fn_BlockUILoader({ action: 'show', target: "#divMain", message: as_Utilities.fn_GetLabel(3784) });
        var l_objParam = {
            languageId: as_Session.fn_GetSession("CurrentUserSession").Language,
            userId: as_Session.fn_GetSession("CurrentUserSession").UserId,
            customerId: as_Session.fn_GetSession("CurrentUserSession").CustomerId,
            groupId: as_Session.fn_GetSession("CurrentUserSession").UserGroupId,
            roleId: as_Session.fn_GetSession("CurrentUserSession").UserRoleId,
            datasetIds: p_scope.cs_AnalysisModel.AssosiatedDataset
        };

        /* This service call will return the full information of selected dataset */
        as_UnifiedEngine.fn_GetDatasetInformation(l_objParam).success(p_callback).error(function (ex) {
            cs_toolkit.fn_BlockUILoader({ action: 'hide', target: "#divMain", message: as_Utilities.fn_GetLabel(3784) });
        });
    }


}]);






