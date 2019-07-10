am_DucenApp.factory('af_TextHelper',
    ['$controller', '$rootScope', '$compile', '$timeout', 'as_Session', 'as_Utilities', 'as_Dataset', 'as_GlobalSettings', 'as_Scheduler', 'as_Job', 'as_AnalysisService',
        function (p_controller, p_rootScope, p_compile, p_timeout, as_Session, as_Utilities, as_Dataset, as_GlobalSettings, as_Scheduler, as_Job, as_AnalysisService) {
            var l_objScope;
            var l_arrHelpers;
            function fn_startInjecting() {
                p_controller(l_arrHelpers, {
                    $scope: l_objScope,
                    $rootScope: p_rootScope,
                    $compile: p_compile,
                    $timeout: p_timeout,
                    as_Session: as_Session,
                    as_Utilities: as_Utilities,
                    as_Dataset: as_Dataset,
                    as_GlobalSettings: as_GlobalSettings,
                    as_Scheduler: as_Scheduler,
                    as_Job: as_Job,
                    as_AnalysisService: as_AnalysisService
                });
            }
            return {
                $injectHelpers: function (p_scope, p_arrHelpers) {
                    l_objScope = p_scope;
                    l_arrHelpers = p_arrHelpers;
                    fn_startInjecting();
                }
            }

        }]);