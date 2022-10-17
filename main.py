import sys
from src.flow_manager import FlowManager


def main(flow_job, params):
    fm = FlowManager()
    flow_job_list = fm.get_flow_list()

    if flow_job_list.get(flow_job):
        flow_job_list.get(flow_job)(params).run()


if __name__ == "__main__":

    try:
        args = sys.argv[1]
    except:
        args = None

    if args:
        try:
            params = sys.argv[2]
        except:
            params = None

        try:
            main(args, params)
        except Exception as e:
            print(e)
